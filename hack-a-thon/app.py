import openai
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from io import BytesIO
from parser import extract_blocks_and_names

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    code = request.form.get('code')
    customer = request.form.get('customer')
    blocks, names, helpers = extract_blocks_and_names(code)
    new_blocks = []
    for block in blocks:
        new_block = "Give a general short description of what this function is accomplishing not using too much technical language: " + block
        new_blocks.append(new_block)

    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    gpt_responses = []
    for prompt in new_blocks:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [
                {"role": "user", "content": prompt}
            ]
        )
        gpt_responses.append(response.choices[0]["message"]["content"])

    buffer = BytesIO()

    # Create a new SimpleDocTemplate object and a styles dictionary.
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Add a title style
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=20, textColor=colors.black, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='HeaderStyle', fontSize=14, textColor=colors.black, alignment=TA_CENTER))

    # Add a smaller style for the helper text
    styles.add(ParagraphStyle(name='HelperStyle', fontSize=10, textColor=colors.grey, alignment=TA_CENTER))

    elements = []

    elements.append(Paragraph(f'{customer} Code Description', styles['TitleStyle']))
    elements.append(Spacer(1, 42))

    for name, gpt_response in zip(names, gpt_responses):
        elements.append(Paragraph(f'<strong>{name}</strong>', styles['HeaderStyle']))

        if name in helpers:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(f'<i>Helper function for {", ".join(helpers[name])}</i>', styles['HelperStyle']))

        elements.append(Paragraph(gpt_response, styles['BodyText']))
        elements.append(Spacer(1, 20))

    doc.build(elements)

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='code_description.pdf')

if __name__ == '__main__':
    app.run(port=5000)