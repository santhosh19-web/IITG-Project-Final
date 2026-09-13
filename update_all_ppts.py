import glob
from pptx import Presentation
from pptx.util import Pt

details_text = "Name: K.Santhosh Reddy\nCohort: 4 Batch A2\nMentor: Mr. Vamshi"

def set_times_new_roman(prs):
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            
            # Check if this shape is the one we injected earlier (contains the exact details)
            # Or if it's the subtitle from Day 6.
            # If so, clear the text entirely to remove it from the title slide.
            full_text = "\n".join([p.text for p in shape.text_frame.paragraphs])
            if "Name: K.Santhosh Reddy" in full_text:
                shape.text_frame.clear() # Removes all paragraphs and text from this shape
                continue
                
            for paragraph in shape.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.name = "Times New Roman"
                    
def add_details_slide(prs):
    # Add a new slide at the end for the details
    slide_layout = prs.slide_layouts[1] # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    
    title_shape = slide.shapes.title
    title_shape.text = "Project Details"
    if title_shape.text_frame.paragraphs and title_shape.text_frame.paragraphs[0].runs:
        title_shape.text_frame.paragraphs[0].runs[0].font.name = "Times New Roman"
    
    body_shape = slide.placeholders[1]
    tf = body_shape.text_frame
    tf.clear()
    
    for line in details_text.split('\n'):
        p = tf.add_paragraph()
        p.text = line
        p.space_after = Pt(14)
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(28)

def main():
    pptx_files = glob.glob("*.pptx")
    for file in pptx_files:
        try:
            prs = Presentation(file)
            set_times_new_roman(prs)
            add_details_slide(prs)
            prs.save(file)
            print(f"  [x] Updated {file}")
        except Exception as e:
            print(f"  [!] Failed to update {file}: {e}")

if __name__ == "__main__":
    main()
