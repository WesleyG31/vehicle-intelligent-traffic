from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os
import glob

class TrafficPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Urban Traffic Report', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 9)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_summary(self, total_veh, avg_speed, total_inf):
        self.set_font("Arial", size=12)
        self.cell(0, 10, f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
        self.ln(5)
        self.cell(0, 10, f"Total number of vehicles detected: {total_veh}", ln=True)
        self.cell(0, 10, f"Overall average speed: {avg_speed:.2f} km/h", ln=True)
        self.cell(0, 10, f"Speeding violations: {total_inf}", ln=True)
        self.ln(10)

    def add_image(self, path, title):
        if os.path.exists(path):
            self.set_font("Arial", 'B', 12)
            self.cell(0, 10, title, ln=True)
            self.image(path, w=170)
            self.ln(10)

    def add_table(self, data, title):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", size=10)
        for row in data:
            self.cell(0, 10, ' | '.join(str(x) for x in row), ln=True)

    def add_all_images_from_folder(self, folder_path):
        image_paths = sorted(glob.glob(os.path.join(folder_path, "*.png")))

        if not image_paths:
            self.set_font("Arial", size=10)
            self.cell(0, 10, "There's no graph", ln=True)
            return

        for img_path in image_paths:
            title = os.path.splitext(os.path.basename(img_path))[0]  
            title = title.replace("_", " ").capitalize()
            self.add_image(img_path, title)

def generate_report(track_csv,violations_csv,output_path_data_analyzed,output_pdf):
    # Load data
    track = pd.read_csv(track_csv)
    violations = pd.read_csv(violations_csv)

    total_veh = track["id"].nunique()
    avg_speed = track["speed_kph"].mean()
    total_inf = violations["violation"].sum()

    # create pdf
    pdf = TrafficPDF()
    pdf.add_page()
    pdf.add_summary(total_veh, avg_speed, total_inf)
    pdf.add_all_images_from_folder(output_path_data_analyzed)


    # get the plates from violations
    infractores = violations[(violations["violation"] == True) & (violations["plate"].notna())]

    # group by ID
    placas_infractores = infractores.groupby("id").first().reset_index()

    # data -> list
    data = placas_infractores[["id", "plate"]].values.tolist()

    if data:
        pdf.add_table(data, "License plates with speeding violation")


    output_path = output_pdf
    pdf.output(output_path)
    print(f"PDF ready: {output_path}")
