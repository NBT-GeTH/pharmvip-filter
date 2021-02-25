from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from subprocess import Popen, PIPE
from PIL import ImageTk, Image # pip install PIL
from tkinter import Menu
try:
    import tkinter as tk
except:
    import Tkinter as tk
import webbrowser # pip install webbrowser
import threading
import datetime
import time
import os
import re

# font default
LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

# Create GUI
class GuiFillter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageVCF, PageBAM):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageVCF)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Page VCF
class PageVCF(tk.Frame):
    def __init__(self, parent, controller):
        entryText_vcf1 = tk.StringVar()
        entryText_vcf2 = tk.StringVar()
        CheckVar_vcf1 = tk.BooleanVar()
        CheckVar_vcf2 = tk.BooleanVar()
        tk.Frame.__init__(self, parent)
        frame_btn = tk.Frame(self, width=480, height=40)
        frame_btn.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        button1 = tk.Button(frame_btn, text="VCF Page", width=10, bd=5, activeforeground='white',
                            activebackground="blue",
                            command=lambda: controller.show_frame(PageVCF))
        button1.place(x=10, y=10)
        button2 = tk.Button(frame_btn, text="BAM Page", width=10, bd=5, activeforeground='white',
                            activebackground="black",
                            command=lambda: controller.show_frame(PageBAM))
        button2.place(x=110, y=10)
        # VCF
        vcf_label_frame = tk.LabelFrame(self, text="VCF", font=("Times"), width=460, height=430)
        vcf_label_frame.grid(row=1, column=0, padx=5, pady=5, ipadx=0, ipady=0)
        file_label_frame = tk.Label(vcf_label_frame, text="Input File Path:")
        file_label_frame.place(x=5, y=20)
        output_file = tk.Entry(vcf_label_frame, width=38, textvariable=entryText_vcf1, relief=tk.RIDGE, state='disabled')
        output_file.place(x=104, y=20)

        def UploadAction_vcf1():
            filename = filedialog.askopenfilename(title="Select A File", filetypes=(
                ("Variant Call Format files", "*.gz"), ("Variant Call Format files", "*.vcf"), ("All files", "*.*")))
            # print('Selected:', filename)
            entryText_vcf1.set(filename)
            return filename

        file_btn_frame1 = tk.Button(vcf_label_frame, text="Browse", width=10, command=UploadAction_vcf1)
        file_btn_frame1.place(x=350, y=18)
        file_label_frame = tk.Label(vcf_label_frame, text="Output File Path:")
        file_label_frame.place(x=5, y=66)
        output_file = tk.Entry(vcf_label_frame, width=38, textvariable=entryText_vcf2, relief=tk.RIDGE, state='disabled')
        output_file.place(x=104, y=66)

        def UploadAction_vcf2():
            pathname = filedialog.askdirectory()
            entryText_vcf2.set(pathname)
            return pathname

        file_btn_frame2 = tk.Button(vcf_label_frame, text="Browse", width=10, command=UploadAction_vcf2)
        file_btn_frame2.place(x=350, y=64)
        head_label_vcf = tk.Label(vcf_label_frame, text="Select Genes type", font=("Times", 11, "bold"))
        head_label_vcf.place(x=5, y=105)
        chk_vcf_ex1 = tk.Checkbutton(vcf_label_frame, variable=CheckVar_vcf1)
        chk_vcf_ex1.place(x=2, y=135)
        cpic_vcf_frame = tk.LabelFrame(vcf_label_frame, bd=3, width=180, height=211)
        cpic_vcf_frame.place(x=27, y=140)
        chk_vcf_ex2 = tk.Checkbutton(vcf_label_frame, variable=CheckVar_vcf2)
        chk_vcf_ex2.place(x=225, y=135)
        pgx_vcf_frame = tk.LabelFrame(vcf_label_frame, bd=3, width=180, height=211)
        pgx_vcf_frame.place(x=250, y=140)
        content_vcf_label = tk.Label(cpic_vcf_frame, text="• CPIC GENES", font=("Times", 9, "bold"))
        content_vcf_label.place(x=3, y=3)
        content_vcf_label = tk.Label(cpic_vcf_frame, text="- CACNA1S\n"
                                                          "- CYP2B6\n"
                                                          "- CYP2C9\n"
                                                          "- CYP3A5\n"
                                                          "- DPYD\n"
                                                          "- IFNL3\n"
                                                          "- RYR1\n"
                                                          "- TPMT\n"
                                                          "- VKORC1\n"
                                                          "- CFTR", justify="left")
        content_vcf_label.place(x=11, y=22)
        content_vcf_label = tk.Label(cpic_vcf_frame, text="- CYP2C19\n"
                                                          "- CYP4F2\n"
                                                          "- G6PD\n"
                                                          "- NUDT15\n"
                                                          "- SLCO1B1\n"
                                                          "- UGT1A1\n", justify="left")
        content_vcf_label.place(x=88, y=22)
        content_vcf_label = tk.Label(pgx_vcf_frame, text="• PGx GENES", font=("Times", 9, "bold"))
        content_vcf_label.place(x=3, y=3)
        content_vcf_label = tk.Label(pgx_vcf_frame, text="- CPIC\n"
                                                         "- DrugBank\n"
                                                         "- FDA Biomarker\n"
                                                         "- iPLEX PGx Pro Panel\n"
                                                         "- Korean Target seq\n"
                                                         "- PGRNseq\n"
                                                         "- PGx testing\n"
                                                         "- PharmGKB clinical variant\n"
                                                         "   data\n"
                                                         "- PharmGKB VIPs:66\n"
                                                         "- TruGenome Illumina", justify="left")
        content_vcf_label.place(x=11, y=22)

        commandText = tk.Frame(self, width=480, height=160)
        commandText.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        progressBar = tk.Frame(self, width=480, height=40)
        progressBar.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        class ConsoleVCF(tk.Frame):
            """Simple console that can execute bash commands"""

            def __init__(self, master, *args, **kwargs):
                tk.Frame.__init__(self, master, *args, **kwargs)
                # commandText = tk.Frame(self, width=480, height=160)
                # commandText.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
                self.labelText = tk.StringVar()
                self.text = ScrolledText(commandText,
                                         width=55,
                                         height=10,
                                         state=tk.DISABLED,
                                         bg="black",
                                         fg="#08c614",
                                         insertbackground="#08c614",
                                         selectbackground="#f01c1c")
                self.text.pack(side=tk.TOP, expand=True, fill=tk.X)

                self.pb = ttk.Progressbar(progressBar, orient="horizontal", length=435, mode="determinate")
                self.pb.place(x=8, y=7)

                self.loadtime = tk.Label(progressBar, textvariable=self.labelText)
                self.loadtime.place(x=444, y=7)

                self.labelText.set("")
                # bash command, for example 'ping localhost' or 'pwd'
                # that will be executed when "Execute" is pressed
                self.command = ""
                self.popen = None  # will hold a reference to a Popen object
                self.running = False  # True if the process is running

            def btn_already(self):
                button1["state"] = tk.NORMAL
                button2["state"] = tk.NORMAL
                chk_vcf_ex1["state"] = tk.NORMAL
                chk_vcf_ex2["state"] = tk.NORMAL
                file_btn_frame1["state"] = tk.NORMAL
                file_btn_frame2["state"] = tk.NORMAL
                vcf_btn_process["state"] = tk.NORMAL

            def btn_process(self):
                button1["state"] = tk.DISABLED
                button2["state"] = tk.DISABLED
                chk_vcf_ex1["state"] = tk.DISABLED
                chk_vcf_ex2["state"] = tk.DISABLED
                file_btn_frame1["state"] = tk.DISABLED
                file_btn_frame2["state"] = tk.DISABLED
                vcf_btn_process["state"] = tk.DISABLED

            def clear_text(self):
                """Clears the Text widget"""
                self.text.config(state="normal")
                self.text.delete(1.0, "end-1c")
                self.text.config(state="disabled")

            def show(self, message):
                """Inserts message into the Text wiget"""
                self.text.config(state="normal")
                self.text.insert("end", message)
                self.text.see("end")
                self.text.config(state="disabled")
                if ">>> Not found Conda" in message:
                    self.labelText.set("0%")
                    self.pb['value'] = 0
                    self.update_idletasks()
                elif "Wait Install Tabix ......" in message or ">>> Tabix Already Installed" in message:
                    self.labelText.set("5%")
                    self.pb['value'] = 5
                    self.update_idletasks()
                elif "Wait Install Samtools ......" in message or ">>> Samtools Already Installed" in message:
                    self.labelText.set("10%")
                    self.pb['value'] = 10
                    self.update_idletasks()
                elif "Wait Install Bcftools ......" in message or ">>> Bcftools Already Installed" in message:
                    self.labelText.set("15%")
                    self.pb['value'] = 15
                    self.update_idletasks()
                elif ">>> Start filtering CPIC and PGx Genes...." in message or ">>> Start filtering CPIC Genes...." in message or ">>> Start filtering PGx Genes...." in message:
                    self.labelText.set("20%")
                    self.pb['value'] = 20
                    self.update_idletasks()
                elif ">>> Creating Folder for filtered file...." in message:
                    self.labelText.set("25%")
                    self.pb['value'] = 25
                    self.update_idletasks()
                elif ">>> Compressing file for extracting...." in message:
                    self.labelText.set("35%")
                    self.pb['value'] = 35
                    self.update_idletasks()
                elif ">>> Indexing file." in message:
                    self.labelText.set("45%")
                    self.pb['value'] = 45
                    self.update_idletasks()
                elif ">>> Extracting...." in message:
                    self.labelText.set("70%")
                    self.pb['value'] = 70
                    self.update_idletasks()
                elif ">>> Sorting...." in message:
                    self.labelText.set("80%")
                    self.pb['value'] = 80
                    self.update_idletasks()
                elif ">>> Compressing final file...." in message:
                    self.labelText.set("90%")
                    self.pb['value'] = 90
                    self.update_idletasks()
                elif ">>> Indexing final file...." in message:
                    self.labelText.set("95%")
                    self.pb['value'] = 95
                    self.update_idletasks()
                elif "Process completed...." in message:
                    self.labelText.set("99%")
                    self.pb['value'] = 99
                    self.update_idletasks()

            def start_thread(self, event=None):
                """Starts a new thread and calls process"""

                self.clear_text()

                self.btn_process()

                self.check_cpic = CheckVar_vcf1.get()
                self.check_pgx = CheckVar_vcf2.get()
                self.process_time = 0
                self.allele_matcher_start_time = time.time()

                try:
                    path_tmp = "/mnt/_tmp"
                    check_path_File = entryText_vcf1.get()
                    x1 = re.search(r"(.:)(.+)", check_path_File)
                    drive = x1.group(1)
                    drive1 = x1.group(1)[0]
                    drive_name1 = x1.group(2)
                    set_check_path_File = path_tmp
                    check_path_linux = set_check_path_File + drive_name1
                    head, tail = os.path.split(check_path_File)
                    filename = tail.split('.')

                    select_path_File = entryText_vcf2.get()
                    path_win = entryText_vcf2.get()
                    x2 = re.search(r"(.:)(.+)", select_path_File)
                    drive2 = x2.group(1)[0]
                    drive_name2 = x2.group(2)
                    set_select_path_File = "/mnt/" + drive2.lower()
                    select_path_linux = set_select_path_File + drive_name2
                    if ' ' in check_path_linux or ' ' in select_path_linux:
                        check_path_linux = check_path_linux.replace(" ", ",")
                        select_path_linux = select_path_linux.replace(" ", ",")
                        path_win = path_win.replace(" ", ",")
                    else:
                        pass
                except AttributeError:
                    self.show("Please select a file or file address.\n\n")
                    self.btn_already()
                    self.stop_cmd()

                self.stop_cmd()
                self.running = True

                if os.path.isfile('{}'.format(check_path_File)) == True and os.path.isdir('{}'.format(select_path_File)) == True:
                    self.setting = f"bash ./publics/setting.sh {drive}"
                    if self.check_cpic == True and self.check_pgx == True:
                        self.command = f"bash ./publics/filter_CPIC-PGx.sh {check_path_linux} {select_path_linux} {filename[0]} {path_win}"
                    elif self.check_cpic == True and self.check_pgx == False:
                        self.command = f"bash ./publics/filter_CPIC.sh {check_path_linux} {select_path_linux} {filename[0]} {path_win}"
                    elif self.check_cpic == False and self.check_pgx == True:
                        self.command = f"bash ./publics/filter_PGx.sh {check_path_linux} {select_path_linux} {filename[0]} {path_win}"
                    else:
                        self.show("Please Select Type Genes.\n\n")
                        self.btn_already()
                        self.stop_cmd()
                else:
                    self.show("Please check that the files and folders are correct.\n\n")
                    self.btn_already()
                    self.stop_cmd()

                # self.process is called by the Thread's run method
                threading.Thread(target=self.process).start()

            def process(self):
                """Runs in an infinite loop until self.running is False"""
                while self.running:
                    self.execute()

            def stop_cmd(self):
                """Stops an eventual running process"""
                if self.popen:
                    try:
                        self.popen.kill()
                    except ProcessLookupError:
                        pass
                self.running = False

            def execute(self):
                """Keeps inserting line by line into self.text
                the output of the execution of self.command"""
                try:
                    self.show("Note: Please Install Ubuntu on your computer. \nInstallation steps -> https://ubuntu.com/tutorials/ubuntu-on-windows#1-overview\n")
                    # self.popen is a Popen object
                    cmdSet = os.system('cmd /c "ubuntu config --default-user root"')
                    self.popen = Popen(self.setting, stdout=PIPE, shell=True)
                    lines_iterator = iter(self.popen.stdout.readline, b"")
                    while self.popen.poll() is None:
                        for line in lines_iterator:
                            self.show(line.decode("utf-8"))

                    self.popen = Popen(self.command, stdout=PIPE, shell=True)
                    lines_iterator = iter(self.popen.stdout.readline, b"")
                    while self.popen.poll() is None:
                        for line in lines_iterator:
                            self.show(line.decode("utf-8"))

                    runTime = time.time() - self.allele_matcher_start_time
                    looptime = f"\n> run pharmvip_guideline allele_matcher successfully \n  in {str(datetime.timedelta(seconds=int(runTime)))} \n"
                    self.show(looptime)
                    self.labelText.set("100%")
                    self.pb['value'] = 100
                    self.update_idletasks()
                except FileNotFoundError:
                    self.show("Unknown command: " + self.command + "\n\n")
                except IndexError:
                    self.show("No command entered\n\n")

                self.btn_already()
                self.stop_cmd()

        vcf_cmd = ConsoleVCF(self)
        vcf_cmd.place(x=0, y=480)

        # Process
        vcf_btn_process = tk.Button(vcf_label_frame, text="Next", width=10, command=vcf_cmd.start_thread)
        vcf_btn_process.place(x=348, y=363)

# Page BAM
class PageBAM(tk.Frame):
    def __init__(self, parent, controller):
        entryText_bam1 = tk.StringVar()
        entryText_bam2 = tk.StringVar()
        CheckVar_bam1 = tk.BooleanVar()
        CheckVar_bam2 = tk.BooleanVar()
        tk.Frame.__init__(self, parent)
        frame_btn = tk.Frame(self, width=480, height=40)
        frame_btn.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        button1 = tk.Button(frame_btn, text="VCF Page", width=10, bd=5, activeforeground='white',
                            activebackground="blue",
                            command=lambda: controller.show_frame(PageVCF))
        button1.place(x=10, y=10)

        button2 = tk.Button(frame_btn, text="BAM Page", width=10, bd=5, activeforeground='white',
                            activebackground="black",
                            command=lambda: controller.show_frame(PageBAM))
        button2.place(x=110, y=10)
        # BAM
        bam_label_frame = tk.LabelFrame(self, text="BAM", font=("Times"), width=460, height=430)
        bam_label_frame.grid(row=1, column=0, padx=5, pady=5, ipadx=0, ipady=0)
        file_label_frame = tk.Label(bam_label_frame, text="Input File Path: ")
        file_label_frame.place(x=22, y=20)
        output_file = tk.Entry(bam_label_frame, width=36, textvariable=entryText_bam1, relief=tk.RIDGE, state='disabled')
        output_file.place(x=120, y=20)

        def UploadAction_bam1():
            filename = filedialog.askopenfilename(title="Select A File",
                                                  filetypes=(("Binary Alignment Map", "*.bam"), ("All files", "*.*")))
            entryText_bam1.set(filename)

        file_btn_frame1 = tk.Button(bam_label_frame, text="Browse", width=10, command=UploadAction_bam1)
        file_btn_frame1.place(x=350, y=18)
        file_label_frame = tk.Label(bam_label_frame, text="Output File Path: ")
        file_label_frame.place(x=22, y=66)
        output_file = tk.Entry(bam_label_frame, width=36, textvariable=entryText_bam2, relief=tk.RIDGE, state='disabled')
        output_file.place(x=120, y=66)

        def UploadAction_bam2():
            pathname = filedialog.askdirectory()
            entryText_bam2.set(pathname)

        file_btn_frame2 = tk.Button(bam_label_frame, text="Browse", width=10, command=UploadAction_bam2)
        file_btn_frame2.place(x=350, y=64)

        head_label_bam = tk.Label(bam_label_frame, text="Select Genes type", font=("Times", 11, "bold"))
        head_label_bam.place(x=22, y=105)
        chk_bam_ex1 = tk.Checkbutton(bam_label_frame, variable=CheckVar_bam1)
        chk_bam_ex1.place(x=22, y=135)
        detail_bam_frame1 = tk.LabelFrame(bam_label_frame, bd=3, width=355, height=66)
        detail_bam_frame1.place(x=49, y=140)
        content_bam_label = tk.Label(detail_bam_frame1, text="• HLA GENES", font=("Times", 9, "bold"))
        content_bam_label.place(x=3, y=3)
        content_bam_label = tk.Label(detail_bam_frame1, text="- The HLA and adverse Drug Reaction Database\n"
                                                             "- HLA sequence library: The IPD-IMGT/HLA Database",
                                     justify="left")
        content_bam_label.place(x=11, y=22)
        chk_bam_ex2 = tk.Checkbutton(bam_label_frame, variable=CheckVar_bam2)
        chk_bam_ex2.place(x=22, y=215)
        detail_bam_frame2 = tk.LabelFrame(bam_label_frame, bd=3, width=355, height=33)
        detail_bam_frame2.place(x=49, y=220)
        content_bam_label = tk.Label(detail_bam_frame2, text="• CYP2D6 GENES", font=("Times", 9, "bold"))
        content_bam_label.place(x=3, y=3)

        commandText = tk.Frame(self, width=460, height=160)
        commandText.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        progressBar = tk.Frame(self, width=480, height=40)
        progressBar.grid(row=3, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        class ConsoleBAM(tk.Frame):
            """Simple console that can execute bash commands"""

            def __init__(self, master, *args, **kwargs):
                tk.Frame.__init__(self, master, *args, **kwargs)
                self.labelText = tk.StringVar()
                self.text = ScrolledText(commandText,
                                         width=55,
                                         height=10,
                                         state=tk.DISABLED,
                                         bg="black",
                                         fg="#08c614",
                                         insertbackground="#08c614",
                                         selectbackground="#f01c1c")
                self.text.pack(side=tk.TOP, expand=True, fill=tk.X)

                self.pb = ttk.Progressbar(progressBar, orient="horizontal", length=435, mode="determinate")
                self.pb.place(x=8, y=7)

                self.loadtime = tk.Label(progressBar, textvariable=self.labelText)
                self.loadtime.place(x=444, y=7)

                self.labelText.set("")

                # bash command, for example 'ping localhost' or 'pwd'
                # that will be executed when "Execute" is pressed
                self.command = ""
                self.popen = None  # will hold a reference to a Popen object
                self.running = False  # True if the process is running

            def btn_already(self):
                button1["state"] = tk.NORMAL
                button2["state"] = tk.NORMAL
                chk_bam_ex1["state"] = tk.NORMAL
                chk_bam_ex2["state"] = tk.NORMAL
                file_btn_frame1["state"] = tk.NORMAL
                file_btn_frame2["state"] = tk.NORMAL
                bam_btn_process["state"] = tk.NORMAL

            def btn_process(self):
                button1["state"] = tk.DISABLED
                button2["state"] = tk.DISABLED
                chk_bam_ex1["state"] = tk.DISABLED
                chk_bam_ex2["state"] = tk.DISABLED
                file_btn_frame1["state"] = tk.DISABLED
                file_btn_frame2["state"] = tk.DISABLED
                bam_btn_process["state"] = tk.DISABLED

            def clear_text(self):
                """Clears the Text widget"""
                self.text.config(state="normal")
                self.text.delete(1.0, "end-1c")
                self.text.config(state="disabled")

            def show(self, message):
                """Inserts message into the Text wiget"""
                self.text.config(state="normal")
                self.text.insert("end", message)
                self.text.see("end")
                self.text.config(state="disabled")
                if ">>> Not found Conda" in message:
                    self.labelText.set("0%")
                    self.pb['value'] = 0
                    self.update_idletasks()
                elif "Wait Install Tabix ......" in message or ">>> Tabix Already Installed" in message:
                    self.labelText.set("5%")
                    self.pb['value'] = 5
                    self.update_idletasks()
                elif "Wait Install Samtools ......" in message or ">>> Samtools Already Installed" in message:
                    self.labelText.set("10%")
                    self.pb['value'] = 10
                    self.update_idletasks()
                elif "Wait Install Bcftools ......" in message or ">>> Bcftools Already Installed" in message:
                    self.labelText.set("15%")
                    self.pb['value'] = 15
                    self.update_idletasks()
                elif ">>> Start filtering HLA and CYP2D6 Genes...." in message or ">>> Start filtering HLA Genes...." in message or ">>> Start filtering CYP2D6 Genes...." in message:
                    self.labelText.set("25%")
                    self.pb['value'] = 25
                    self.update_idletasks()
                elif ">>> Creating Folder for filtered file...." in message:
                    self.labelText.set("35%")
                    self.pb['value'] = 35
                    self.update_idletasks()
                elif ">>> Index File...." in message:
                    self.labelText.set("45%")
                    self.pb['value'] = 45
                    self.update_idletasks()
                elif ">>> Extracting...." in message:
                    self.labelText.set("75%")
                    self.pb['value'] = 75
                    self.update_idletasks()
                elif "Process completed...." in message:
                    self.labelText.set("99%")
                    self.pb['value'] = 99
                    self.update_idletasks()

            def start_thread(self, event=None):
                """Starts a new thread and calls process"""

                self.clear_text()

                self.btn_process()

                self.check_hla = CheckVar_bam1.get()
                self.check_cyp2d6 = CheckVar_bam2.get()
                self.process_time = 0
                self.allele_matcher_start_time = time.time()

                try:
                    path_tmp = "/mnt/_tmp"
                    check_path_File = entryText_bam1.get()
                    x1 = re.search(r"(.:)(.+)", check_path_File)
                    drive = x1.group(1)
                    drive1 = x1.group(1)[0]
                    drive_name1 = x1.group(2)
                    set_check_path_File = path_tmp
                    check_path_linux = set_check_path_File + drive_name1
                    head, tail = os.path.split(check_path_File)
                    filename = tail.split('.')

                    select_path_File = entryText_bam2.get()
                    x2 = re.search(r"(.:)(.+)", select_path_File)
                    drive2 = x2.group(1)[0]
                    drive_name2 = x2.group(2)
                    set_select_path_File = "/mnt/" + drive2.lower()
                    select_path_linux = set_select_path_File + drive_name2
                    if ' ' in check_path_linux or ' ' in select_path_linux:
                        check_path_linux = check_path_linux.replace(" ", ",")
                        select_path_linux = select_path_linux.replace(" ", ",")
                    else:
                        pass
                except AttributeError:
                    self.show("Please select a file or file address.\n\n")
                    self.btn_already()
                    self.stop_cmd()

                self.stop_cmd()
                self.running = True

                if os.path.isfile('{}'.format(check_path_File)) == True and os.path.isdir('{}'.format(select_path_File)) == True:
                    self.setting = f"bash ./publics/setting.sh {drive}"
                    if self.check_hla == True and self.check_cyp2d6 == True:
                        self.command = f"bash ./publics/filter_HLA-CYP2D6.sh {check_path_linux} {select_path_linux} {filename[0]}"
                    elif self.check_hla == True and self.check_cyp2d6 == False:
                        self.command = f"bash ./publics/filter_HLA.sh {check_path_linux} {select_path_linux} {filename[0]}"
                    elif self.check_hla == False and self.check_cyp2d6 == True:
                        self.command = f"bash ./publics/filter_CYP2D6.sh {check_path_linux} {select_path_linux} {filename[0]}"
                    else:
                        self.show("Please Select Type Genes.\n\n")
                        self.btn_already()
                        self.stop_cmd()
                else:
                    self.show("Please check that the files and folders are correct.\n\n")
                    self.btn_already()
                    self.stop_cmd()

                # self.process is called by the Thread's run method
                threading.Thread(target=self.process).start()

            def process(self):
                """Runs in an infinite loop until self.running is False"""
                while self.running:
                    self.execute()

            def stop_cmd(self):
                """Stops an eventual running process"""
                if self.popen:
                    try:
                        self.popen.kill()
                    except ProcessLookupError:
                        pass
                self.running = False

            def execute(self):
                """Keeps inserting line by line into self.text
                the output of the execution of self.command"""
                try:
                    self.show("Note: Please Install Ubuntu on your computer. \nInstallation steps -> https://ubuntu.com/tutorials/ubuntu-on-windows#1-overview\n")
                    # self.popen is a Popen objec
                    cmdSet = os.system('cmd /c "ubuntu config --default-user root"')
                    self.popen = Popen(self.setting, stdout=PIPE, shell=True)
                    lines_iterator = iter(self.popen.stdout.readline, b"")
                    while self.popen.poll() is None:
                        for line in lines_iterator:
                            self.show(line.decode("utf-8"))
                    self.popen = Popen(self.command, stdout=PIPE, shell=True)
                    lines_iterator = iter(self.popen.stdout.readline, b"")
                    while self.popen.poll() is None:
                        for line in lines_iterator:
                            self.show(line.decode("utf-8"))

                    runTime = time.time() - self.allele_matcher_start_time
                    looptime = f"\n> run pharmvip_guideline allele_matcher successfully \n  in {str(datetime.timedelta(seconds=int(runTime)))} \n"
                    self.show(looptime)
                    self.labelText.set("100%")
                    self.pb['value'] = 100
                    self.update_idletasks()
                except FileNotFoundError:
                    self.show("Unknown command: " + self.command + "\n\n")
                except IndexError:
                    self.show("No command entered\n\n")

                self.btn_already()
                self.stop_cmd()

        bam_cmd = ConsoleBAM(self)
        bam_cmd.place(x=0, y=480)

        # Process
        bam_btn_process = tk.Button(bam_label_frame, text="Next", width=10, command=bam_cmd.start_thread)
        bam_btn_process.place(x=333, y=363)

if __name__ == "__main__":
    app = GuiFillter()
    app.title('PharmVIP')
    app.iconbitmap('./publics/logomini.ico')

    ### Menu Bar ###
    def popupVersion():
        popup = tk.Toplevel(app)
        popup.wm_title("Version")
        popup.iconbitmap('./publics/logomini.ico')
        # Designate Height and Width of our app
        popup_width = 333
        popup_height = 200
        popup.resizable(width="false", height="false")
        popup.maxsize(width=333, height=200)
        popup.geometry(f'{popup_width}x{popup_height}+{11}+{11}')

        headerText = tk.Frame(popup, width=333, height=60, bg="#324F34")
        headerText.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        contentText = tk.Frame(popup, width=333, height=140)
        contentText.grid(row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0)

        version_label1 = tk.Label(headerText, text="PharmVIP Filter", fg="#d1c49b", font=("Times", 28, "bold"), bg="#324F34")
        version_label1.place(x=11, y=7)
        version_label2 = tk.Label(contentText, text="• Version 0.1.1\n\n"
                                                    "• Build on ...\n\n"
                                                    "• Powered by ...\n\n", font=("Times", 11), justify="left")
        version_label2.place(x=11, y=10)

        image = Image.open("D:/Biobank/GUI/PharmVIP_GUI_v1/logomini.png")
        width, height = image.size
        image = image.resize((round(111 / height * width), round(111)))
        render = ImageTk.PhotoImage(image)
        img = tk.Label(contentText, image=render)
        img.image = render
        img.place(x=200, y=10)

        popup.transient(app)
        popup.grab_set()
        app.wait_window(popup)

    def popupFeedback():
        popup = tk.Toplevel(app)
        popup.wm_title("Feedback")
        popup.iconbitmap('./publics/logomini.ico')
        # Designate Height and Width of our app
        popup_width = 480
        popup_height = 560
        popup.resizable(width="false", height="false")
        popup.maxsize(width=400, height=560)
        popup.geometry(f'{popup_width}x{popup_height}+{11}+{11}')

        frame_header = tk.Frame(popup, width=480, height=100)
        frame_header.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        logo = tk.PhotoImage(file="D:/Biobank/GUI/PharmVIP_GUI_v1/logomini.png")
        logolabel = tk.Label(frame_header, text="logo", image=logo)
        logolabel.place(x=30, y=10)
        headerlabel = tk.Label(frame_header, text="PharmVIP Feedback", fg="#d1c49b", font=("Times", 18, "bold"), bg="#324F34")
        headerlabel.place(x=130, y=30)

        nameVar = tk.StringVar()
        emailVar = tk.StringVar()
        subjectVar = tk.StringVar()

        frame_content = tk.Frame(popup, width=480, height=450)
        frame_content.grid(row=1, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        frame_name = tk.LabelFrame(frame_content, text="Name", font=('Times', 12, "bold"), width=360, height=56)
        frame_name.place(x=20, y=0)
        entry_name = tk.Entry(frame_name, width=56, textvariable=nameVar)
        entry_name.place(x=8, y=2)

        frame_email = tk.LabelFrame(frame_content, text="Email", font=('Times', 12, "bold"), width=360, height=56)
        frame_email.place(x=20, y=75)
        entry_email = tk.Entry(frame_email, width=56, textvariable=emailVar)
        entry_email.place(x=8, y=2)

        frame_subject = tk.LabelFrame(frame_content, text="Subject", font=('Times', 12, "bold"), width=360, height=56)
        frame_subject.place(x=20, y=150)
        entry_subject = tk.Entry(frame_subject, width=56, textvariable=subjectVar)
        entry_subject.place(x=8, y=2)

        frame_comment = tk.LabelFrame(frame_content, text="Comment", font=('Times', 12, "bold"), width=360, height=120)
        frame_comment.place(x=20, y=225)
        textcomment = tk.Text(frame_comment, width=42, height=5)
        textcomment.place(x=8, y=2)
        textcomment.config(wrap='word')

        def submit():
            print('Name: {}'.format(entry_name.get()))
            print('Email: {}'.format(entry_email.get()))
            print('Subject: {}'.format(entry_subject.get()))
            comment = textcomment.get("1.0", tk.END)
            print('Comment: {}'.format(comment))
            messagebox.showinfo(title='Submit', message='Thank you for your Feedback, Your Comments Submited')
            entry_name.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_subject.delete(0, tk.END)
            textcomment.delete(0.1, tk.END)

        def clear():
            messagebox.showinfo(title='clear', message='Do you want to clear?')
            entry_name.delete(0, tk.END)
            entry_email.delete(0, tk.END)
            entry_subject.delete(0, tk.END)
            textcomment.delete(0.1, tk.END)

        submitbutton = tk.Button(popup, text='Submit', font=('Times', 12, "bold"), command=submit)
        submitbutton.place(x=120, y=480)
        clearbutton = tk.Button(popup, text='Clear', font=('Times', 12, "bold"), command=clear)
        clearbutton.place(x=200, y=480)

        popup.transient(app)
        popup.grab_set()
        app.wait_window(popup)
        popup.mainloop()

    def openPharmVIP_website():
        webbrowser.open_new("https://pharmvip.nbt.or.th/pharmvip/?next=/pharmvip/index")

    def openPharmVIP_help():
        webbrowser.open_new("https://pharmvip.nbt.or.th/pharmvip/?next=/pharmvip/index")

    def openPharmVIP_contact():
        webbrowser.open_new("https://intellij-support.jetbrains.com/hc/en-us/requests/new?ticket_form_id=66731&product=PyCharm&build=202.6948.78&os=win-10-64&timezone=Asia/Bangkok")

    menubar = Menu(app)
    # menubar.add_command(label="About".ljust(7), command=popupAbout)
    aboutmenu = Menu(menubar, tearoff=0)
    aboutmenu.add_command(label="Version", command=popupVersion)
    aboutmenu.add_command(label="Go To PharmVIP Website", command=openPharmVIP_website)
    aboutmenu.add_separator()
    aboutmenu.add_command(label="Exit", command=app.destroy)
    menubar.add_cascade(label="About", menu=aboutmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Contact Support", command=openPharmVIP_contact)
    helpmenu.add_separator()
    helpmenu.add_command(label="Feedback", command=popupFeedback)
    menubar.add_cascade(label="Help", menu=helpmenu)
    app.config(menu=menubar)

    # Designate Height and Width of our app
    app_width = 480
    app_height = 700
    app.resizable(width="false", height="false")
    app.maxsize(width=480, height=700)
    app.geometry(f'{app_width}x{app_height}+{0}+{0}')
    app.mainloop()
