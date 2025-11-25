import pandas as pd
from fpdf import FPDF
from matplotlib.figure import Figure
from io import BytesIO
import io
import plotly.io as pio
import img2pdf

# -----------------------------
# DataFrame → PDF
# -----------------------------
def df_to_pdf(df: pd.DataFrame, filename: str) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    col_width = pdf.w / (len(df.columns) + 1)
    row_height = pdf.font_size * 1.5

    # Header
    for col in df.columns:
        pdf.cell(col_width, row_height, str(col), border=1)
    pdf.ln(row_height)

    # Rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)

    pdf.output(filename)
    return filename

# -----------------------------
# DataFrame → Excel
# -----------------------------
def df_to_excel(df: pd.DataFrame, filename: str) -> str:
    df.to_excel(filename, index=False)
    return filename

# -----------------------------
# Convert figure → PNG bytes
# -----------------------------
def save_figure_to_png(fig) -> BytesIO:
    if fig is None:
        return None

    #  Plotly
    if hasattr(fig, "to_image"):
        return pio.to_image(fig, format="png", width=1200, height=800, scale=2)

    # Matplotlib
    if isinstance(fig, Figure):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", facecolor="white")
        buf.seek(0)
        return buf.getvalue()

    return None

# Export multiple figures → PDF
def export_chart_pdf(fig_list, filename: str) -> str:
    images = []

    for fig in fig_list:
        img_bytes = save_figure_to_png(fig)
        if img_bytes is not None:
            images.append(img_bytes)

    if not images:
        raise ValueError("No valid figures to export.")

    # Write colored PDF
    with open(filename, "wb") as f:
        f.write(img2pdf.convert(images))

    return filename
