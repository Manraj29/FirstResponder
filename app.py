import streamlit as st
import sys
import os
from streamlit_markmap import markmap
from streamlit_js_eval import streamlit_js_eval

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from mentormindflows.main import run_fire_flow, run_incident_flow

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)


def generate_mindmap(prompt):
    query = rf"""
        Study the given report which is {prompt} and generate a summary then please be precise in selecting the data such that it gets to a heirarchical structure. Dont give anything else, i just want to display the structure as a mindmap so be precise please. Dont write anything else, Just return the md file. It is not neccessay to cover all information. dont use triple backticks or ` anywhere. Cover the main topics. Please convert this data into a markdown mindmap format similar to the following example:
        ---
        markmap:
        colorFreezeLevel: 2
        ---

        # Gemini Account Summary

        ## Balances

        - Bitcoin (BTC): 0.1234
        - Ethereum (ETH): 0.5678

        ## Orders

        - Open Orders
        - Buy Order (BTC): 0.01 BTC @ $40,000
        - Trade History
        - Sold 0.1 ETH for USD at $2,500

        ## Resources

        - [Gemini Website](https://www.gemini.com/)
    """
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    response = model.generate_content(query)
    return response.text


# Streamlit UI
st.set_page_config(page_title="First Incident Responder", layout="wide")
st.title("Incident Responder")

# Init session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "crew_status" not in st.session_state:
    st.session_state.crew_status = "idle"
if "report_path" not in st.session_state:
    st.session_state.report_path = ""
if "location_value" not in st.session_state:
    st.session_state.location_value = ""
if "incident_context" not in st.session_state:
    st.session_state.incident_context = {}


def classify_category(description: str, image_file) -> str:
    prompt = (
        "Classify the incident into one of these categories strictly: fire, medical, police, accident, other. "
        "Respond with only one word."
    )
    parts = [prompt, f"\n\nDescription:\n{description}"]
    try:
        if image_file is not None:
            parts.append({"mime_type": image_file.type, "data": image_file.getvalue()})
        model = genai.GenerativeModel("gemini-2.0-flash-001")
        resp = model.generate_content(parts)
        text = (resp.text or "").strip().lower()
        for cat in ("fire", "medical", "police", "accident", "other"):
            if cat in text:
                return cat
    except Exception:
        pass
    return "fire"


def classify_severity(description: str, image_file) -> str:
    prompt = (
        "You are a safety classifier. Classify fire incident severity as one of: low, medium, high. "
        "Base your decision on the description (and image if provided). "
        "Respond with only one word: low, medium, or high."
    )
    parts = [prompt, f"\n\nDescription:\n{description}"]
    try:
        if image_file is not None:
            parts.append({"mime_type": image_file.type, "data": image_file.getvalue()})
        model = genai.GenerativeModel("gemini-2.0-flash-001")
        resp = model.generate_content(parts)
        text = (resp.text or "").strip().lower()
        if "high" in text:
            return "high"
        if "medium" in text:
            return "medium"
        if "low" in text:
            return "low"
    except Exception:
        pass
    return "medium"


col_left, col_right = st.columns([0.55, 0.45])

with col_left:
    st.subheader("Incident Details")
    with st.form("fire_incident_form"):
        name = st.text_input("Reporter Name", placeholder="Jane Doe")
        description = st.text_area("Incident Description", placeholder="Describe what happened...")
        image_file = st.file_uploader("Attach an image (optional)", type=["png", "jpg", "jpeg"])

        use_geo = st.checkbox("Use my browser location", value=True)
        location_value = st.session_state.location_value
        if use_geo and not location_value:
            try:
                coords = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition((p)=>p.coords)",
                                            key="geo",
                                            want_output=True,
                                            timeout=7000)
                if coords and coords.get("latitude") and coords.get("longitude"):
                    location_value = f"{coords['latitude']},{coords['longitude']}"
                    st.session_state.location_value = location_value
            except Exception:
                st.info("Allow location permission in your browser or type your location below.")

        location = st.text_input(
            "Location",
            value=location_value,
            placeholder="Coordinates or address (e.g., Building A, 3rd Floor)",
        )

        submitted = st.form_submit_button(
            label="🚀 Classify & Dispatch",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        try:
            if not name.strip():
                raise ValueError("Please enter your name.")
            if not description.strip():
                raise ValueError("Please enter the incident description.")
            if not location.strip():
                raise ValueError("Please provide a location or enable browser location.")

            with st.spinner("Classifying category & severity with Gemini..."):
                category_pred = classify_category(description.strip(), image_file)
                severity_pred = classify_severity(description.strip(), image_file)

            st.success(f"Predicted category: {category_pred} · severity: {severity_pred}")

            # Kick off crew in background
            from threading import Thread

            def _run_crew():
                try:
                    # Persist context for chat session
                    st.session_state.incident_context = {
                        "username": name.strip(),
                        "description": description.strip(),
                        "location": location.strip(),
                        "category": category_pred,
                        "severity": severity_pred,
                    }

                    # Save uploaded image to a temp file to include in report
                    image_path = None
                    if image_file is not None:
                        import tempfile
                        from pathlib import Path
                        suffix = ".jpg"
                        if image_file.type and image_file.type.endswith("png"):
                            suffix = ".png"
                        fd, tmp_path = tempfile.mkstemp(suffix=suffix)
                        Path(tmp_path).write_bytes(image_file.getvalue())
                        image_path = tmp_path

                    report_path = run_incident_flow(
                        category=category_pred,
                        username=name.strip(),
                        description=description.strip(),
                        location=location.strip(),
                        severity=severity_pred,
                        image_path=image_path,
                    )
                    st.session_state.report_path = report_path
                    st.session_state.crew_status = "completed"
                except Exception as e:
                    st.session_state.crew_status = f"error: {e}"

            st.session_state.crew_status = "running"
            Thread(target=_run_crew, daemon=True).start()

        except ValueError as ve:
            st.error(f"❗ {ve}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")

    # Status & report display
    if st.session_state.crew_status == "running":
        st.info("🚒 Crew is being dispatched and report is being generated...")
    elif st.session_state.crew_status.startswith("error"):
        st.error(st.session_state.crew_status)
    elif st.session_state.crew_status == "completed":
        report_path = st.session_state.report_path
        if report_path and os.path.exists(report_path):
            st.markdown("### 📎 Report Preview")
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()
            st.markdown(report_content, unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name=os.path.basename(report_path),
                mime="text/markdown",
            )

            # Also provide PDF download if available
            try:
                import markdown as md
                from weasyprint import HTML
                html = md.markdown(report_content)
                pdf_bytes = HTML(string=html).write_pdf()
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_bytes,
                    file_name=os.path.splitext(os.path.basename(report_path))[0] + ".pdf",
                    mime="application/pdf",
                )
            except Exception:
                pass

            st.markdown("---")
            st.markdown("### 🧠 MindMap of the Report")
            mindmap_content = generate_mindmap(report_content)
            markmap(mindmap_content)
        else:
            st.warning("⚠️ Report file not found. Please ensure the process completed successfully.")

with col_right:
    st.subheader("Assistant Chat")
    # Seed system context once
    if st.session_state.get("incident_context") and (not st.session_state.chat_history or st.session_state.chat_history[0][0] != "system"):
        ctx = st.session_state.incident_context
        system_msg = (
            f"Context: Incident category={ctx.get('category')}, severity={ctx.get('severity')}, "
            f"location={ctx.get('location')}, reporter={ctx.get('username')}\n"
            f"Description: {ctx.get('description')}"
        )
        st.session_state.chat_history.insert(0, ("system", system_msg))

    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(content)

    user_msg = st.chat_input("Ask for guidance while we process your incident...")
    if user_msg:
        st.session_state.chat_history.append(("user", user_msg))
        with st.chat_message("user"):
            st.markdown(user_msg)

        try:
            model = genai.GenerativeModel("gemini-2.0-flash-001")
            context = (
                "You are an emergency response assistant that reassures the user and provides concise, actionable "
                "guidance. Never tell the user to call emergency numbers; instead, state that authorities are already "
                "being contacted by the system and provide safety steps relevant to fire incidents."
            )
            ctx = st.session_state.get("incident_context", {})
            ctx_text = ""
            if ctx:
                ctx_text = (
                    f"\n\nContext: category={ctx.get('category')}, severity={ctx.get('severity')}, "
                    f"location={ctx.get('location')}, reporter={ctx.get('username')}\nDescription: {ctx.get('description')}\n"
                )
            resp = model.generate_content(f"{context}{ctx_text}\n\nUser: {user_msg}")
            bot_text = (resp.text or "Sorry, I couldn't generate a response.")
        except Exception as e:
            bot_text = f"Error: {e}"

        st.session_state.chat_history.append(("assistant", bot_text))
        with st.chat_message("assistant"):
            st.markdown(bot_text)