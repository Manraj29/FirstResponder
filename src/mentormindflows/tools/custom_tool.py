from typing import Type
import pandas as pd
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class StudentCSVToolInput(BaseModel):
    file_path: str = Field(..., description="Path to the student performance CSV file")
    query_type: str = Field(..., description="Type of query: 'summary', 'full', or 'by_student_id'")
    student_id: int = Field(None, description="Student ID to filter, required if using 'by_student_id'")

class StudentCSVTool(BaseTool):
    name: str = "Student CSV Data Tool"
    description: str = (
        "Tool to analyze student performance CSV data. "
        "Supports full data view, summary statistics, and per-student lookup."
    )
    args_schema: Type[BaseModel] = StudentCSVToolInput

    def _run(self, file_path: str, query_type: str, student_id: int = None) -> str:
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.path.dirname(__file__), file_path)

        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            return f"❌ File not found: {file_path}"
        except Exception as e:
            return f"❌ Error reading file: {e}"

        if query_type == "summary":
            return self._generate_summary(df)

        elif query_type == "full":
            return df.to_string(index=False)

        elif query_type == "by_student_id":
            if student_id is None:
                return "❌ Please provide a student_id when using 'by_student_id'."
            result = df[df['student_id'] == student_id]
            return result.to_string(index=False) if not result.empty else "⚠️ No data found for the given student ID."

        else:
            return "❌ Invalid query_type. Use 'summary', 'full', or 'by_student_id'."

    def _generate_summary(self, df: pd.DataFrame) -> str:
        numeric_df = df.select_dtypes(include='number')
        summary_stats = numeric_df.describe().transpose().round(2)

        # Top and bottom performers based on first numeric column
        main_metric = numeric_df.columns[0]
        top = df.sort_values(by=main_metric, ascending=False).head(3)
        bottom = df.sort_values(by=main_metric, ascending=True).head(3)

        markdown_summary = "### 📊 Summary Statistics\n\n"
        markdown_summary += summary_stats.to_markdown()

        markdown_summary += f"\n\n### 🏅 Top 3 Performers (by '{main_metric}')\n\n"
        markdown_summary += top.head(3).to_markdown(index=False)

        markdown_summary += f"\n\n### ⚠️ Bottom 3 Performers (by '{main_metric}')\n\n"
        markdown_summary += bottom.head(3).to_markdown(index=False)

        return markdown_summary
