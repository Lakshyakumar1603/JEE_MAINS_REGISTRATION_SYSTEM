from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import mysql.connector

# Establish connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Jee_Mains"
)



# Function to create a PDF with a heading, subheading, an image, table, and an outline
def create_pdf_with_image_table_and_outline(filename, image_path):
    # Create a PDF canvas
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Set the position and size for the outline (border)
    width, height = letter  # This gets the dimensions of the letter page size

    # Draw a rectangle outline on the page
    c.setStrokeColorRGB(0, 0, 0)  # Set outline color (black in this case)
    c.setLineWidth(2)  # Set the thickness of the outline
    c.rect(10, 10, width - 20, height - 20)  # Create a border with padding of 10 units from all sides

    # Add the image above the heading
    image_width = 200  # Set the desired width of the image
    image_height = 100  # Set the desired height of the image
    image_x = (width - image_width) / 2  # Center the image horizontally
    image_y = height - 120  # Set the y-coordinate for the image (200 units from the top)

    # Add the image (make sure the image file exists at the given path)
    c.drawImage(image_path, image_x, image_y, width=image_width, height=image_height)

    # Add space between the image and the heading
    space_between_image_and_heading = 15 # Space between the image and the heading text

    # Add the heading text "Jee Mains Examination-2025"
    heading_text = "Jee Mains Examination - 2025"
    c.setFont("Helvetica-Bold", 16)  # Set font and size for heading
    heading_width = c.stringWidth(heading_text, "Helvetica-Bold", 16)  # Get the width of the heading text
    heading_x = (width - heading_width) / 2  # Calculate x position to center the text
    
    # Add space from the top outline (e.g., 50 units from the top)
    top_padding = 50  # Space between the top border and the heading text
    heading_y = image_y - space_between_image_and_heading  # Adjust Y-coordinate for heading
    c.drawString(heading_x, heading_y, heading_text)  # Draw the heading at the new position

    # Add the subheading text "Registration Form"
    subheading_text = "Registration Form"
    c.setFont("Helvetica", 12)  # Set font and size for subheading
    subheading_width = c.stringWidth(subheading_text, "Helvetica", 12)  # Get the width of the subheading text
    subheading_x = (width - subheading_width) / 2  # Calculate x position to center the text
    
    # Add some space between the heading and the subheading (e.g., 20 units below the heading)
    subheading_padding = 20  # Space between heading and subheading
    c.drawString(subheading_x, heading_y - subheading_padding, subheading_text)  # Draw the subheading

    cursor = conn.cursor()
    cursor.execute("select * from candidate where sno=(select max(sno) from candidate)")
    l = cursor.fetchall()
    l=list(l)



    # Create a transposed table with column names horizontally and data vertically
    table_data = [
        ["Feilds","Reg-no","Name","Email","phone","DOB","Gender","Category","Address","state-1","city-1","state-2","city-2","state-3","city-3","Payment"],  # Column headers
        ["Details",l[0][0],l[0][1],l[0][2],l[0][3],l[0][4],l[0][5],l[0][6],l[0][7],l[0][8],l[0][9],l[0][10],l[0][11],l[0][12],l[0][13],l[0][14]]
    ]# Row 4
    
    cursor.close()
    conn.close()

    # Transpose the table (flip rows and columns)
    table_data_transposed = list(zip(*table_data))

    # Create the Table and style it
    col_widths = [150, 200, 200, 250, 200, 200, 200, 350]  # Increase the column widths
    table = Table(table_data_transposed,colWidths=col_widths)  # Define column widths (optional)
    
    # Apply styles to the table
    table.setStyle(TableStyle([
        # Header row styling: Set background color, font style, and text color
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Light blue background for the header row
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),      # White text color for the header row
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),   # Bold font for header row
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),             # Center align all cells
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),       # Regular font for data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Light background for data rows
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),    # Add grid lines around the cells
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),             # Center align the data values
        
        # Padding for all cells by default
        ('TOPPADDING', (0, 0), (-1, -1), 5),               # Padding from the top inside cells
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),            # Padding from the bottom inside cells
        ('LEFTPADDING', (0, 0), (-1, -1), 5),              # Padding from the left inside cells
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),             # Padding from the right inside cells
        
        # Specific padding adjustments for certain cells
        ('TOPPADDING', (1, 2), (1, 2), 10),  # More padding above "Date_Of_Birth"
        ('BOTTOMPADDING', (1, 2), (1, 2), 10),  # More padding below "Date_Of_Birth"
        ('TOPPADDING', (1, 2), (1, 2), 10),  # More padding above "Email"
        ('BOTTOMPADDING', (1, 2), (1, 2), 10),  # More padding below "Email"
    ]))

    # Increase space between the heading and the table
    space_between_heading_and_table = 400  # Add 50 units of space between the heading and the table
    # Calculate the width of the table
    
    table_width = 350  # Calculate the total table width
    
    # Position the table below the heading with extra space
    table_x = (width - table_width) / 2  # Left margin for the table
    table_y = heading_y - space_between_heading_and_table - 60  # Adjust Y-coordinate for the table position
    
    # Draw the table onto the canvas
    table.wrapOn(c, width, height)
    table.drawOn(c, table_x, table_y)

    # Save the PDF
    c.save()

# Specify the output filename and image path
filename = "pdf_with_styled_transposed_table.pdf"
image_path = "logo"  # Replace this with the actual path to your image

# Call the function to create the PDF with image, heading, subheading, transposed table, and outline
create_pdf_with_image_table_and_outline(filename, image_path)

print(f"PDF with styled transposed table and outline created: {filename}")
