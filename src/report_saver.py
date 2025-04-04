from fpdf import FPDF
from PIL import Image
import os

def save_to_pdf(text_list, image_path, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add text content
    for text in text_list:
        pdf.multi_cell(0, 10, txt=text)
        pdf.ln(5)  # Add space between paragraphs
    
    # Add image if exists
    if os.path.exists(image_path):
        try:
            # Get image dimensions to scale properly
            with Image.open(image_path) as img:
                img_width, img_height = img.size
                
            # Scale image to fit page width (180mm) while maintaining aspect ratio
            max_width = 180  # in mm (about 7 inches)
            scale_factor = max_width / img_width
            scaled_height = img_height * scale_factor
            
            # Position image below text
            pdf.image(image_path, x=10, y=pdf.get_y(), 
                     w=max_width, h=scaled_height)
        except Exception as e:
            print(f"Could not add image: {str(e)}")
    else:
        print(f"Image not found at {image_path}")
    
    # Clickable link for 3D visuals
    pdf.write(5, "Click to open 3D visuals:- ")
    pdf.set_text_color(0, 0, 255)  # Blue text
    pdf.set_font(style='U')  # Underline
    pdf.cell(0, 5, "conflict_3d", link="conflict_3d.html")
    
    pdf.output(output_file)