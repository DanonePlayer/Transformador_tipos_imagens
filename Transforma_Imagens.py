import tkinter as tk
import tkinter.filedialog as fd
from PIL import Image
import re
from pdf2image import convert_from_path
from tkinter import messagebox
from tkinter.ttk import Progressbar

class Tela:
    def __init__(self, master):
        self.janelaprincipal = master
        self.janelaprincipal.title("Convert Extensões")
        self.janelaprincipal.geometry("450x500")
        self.janelaprincipal.resizable(width=0, height=0)

        self.frm_esquerdo = tk.Frame(self.janelaprincipal, bg="#E0E0E0", width=450, height=500)
        self.frm_esquerdo.grid(column=0, row=0)

        self.photo_Vector = tk.PhotoImage(file="Imagens/Vector.png")

        self.button_escolher_arquivos = tk.Button(self.frm_esquerdo, text="Selecionar Arquivos        ", overrelief=tk.RIDGE, bg="#D1AE6C", command=self.arquivos, fg="#000000", width=178, height=30, image=self.photo_Vector, compound = tk.RIGHT)
        self.button_escolher_arquivos.place(x=140, y=190)

        self.photo = tk.PhotoImage(file="Imagens/logo.png")
        self.lbl_photo = tk.Label(self.frm_esquerdo, image=self.photo, bg="#E0E0E0")
        self.lbl_photo.place(x=168, y=30)


        self.lbl_escolha_tipo = tk.Label(self.frm_esquerdo, text="Escolha o tipo do arquivo final", bg="#E0E0E0", fg="#000000")
        self.lbl_escolha_tipo.place(x=140, y=250)

        self.radio_valor = tk.IntVar()

        self.bntR_jpeg = tk.Radiobutton(self.frm_esquerdo, text="JPEG", variable = self.radio_valor, value=1, bg="#D1AE6C", font=("Open Sans", 9), activebackground="blue")
        self.bntR_jpeg.place(x=60, y=320)
        self.bntR_png = tk.Radiobutton(self.frm_esquerdo, text="PNG", variable = self.radio_valor, value=2, bg="#D1AE6C", font=("Open Sans", 9))
        self.bntR_png.place(x=140, y=320)
        self.bntR_JPG = tk.Radiobutton(self.frm_esquerdo, text="JPG", variable = self.radio_valor, value=3, bg="#D1AE6C", font=("Open Sans", 9))
        self.bntR_JPG.place(x=214, y=320)
        self.bntR_ico = tk.Radiobutton(self.frm_esquerdo, text="ICO", variable = self.radio_valor, value=4, bg="#D1AE6C", font=("Open Sans", 9))
        self.bntR_ico.place(x=288, y=320)
        self.bntR_pdf = tk.Radiobutton(self.frm_esquerdo, text="PDF", variable = self.radio_valor, value=5, bg="#D1AE6C", font=("Open Sans", 9))
        self.bntR_pdf.place(x=360, y=320)


        self.photo_Pasta = tk.PhotoImage(file="Imagens/pasta.png")

        self.button_caminho = tk.Button(self.frm_esquerdo, text="Pasta de Destino    ", overrelief=tk.RIDGE, bg="#D1AE6C", activebackground="#008080", command=self.caminho, fg="#000000", width=140, height=30, image=self.photo_Pasta, compound = tk.RIGHT)
        self.button_caminho.place(x=70, y=410)

        self.photo_convert = tk.PhotoImage(file="Imagens/setas.png")

        self.button = tk.Button(self.frm_esquerdo, text="CONVERTER      ", overrelief=tk.RIDGE, bg="#D1AE6C", activebackground="#008080", command=self.convert, font=('Open Sans', 9), fg="#000000", width=140, height=30, image=self.photo_convert, compound = tk.RIGHT)
        self.button.place(x=260, y=410)

        self.salva_arquivos = False
        self.escolheu_arquivos = False

    def arquivos(self):
        self.count_arq = 0
        self.arquivos_escolhidos = fd.askopenfilenames(initialdir="")
        # print(self.arquivos_escolhidos)
        for tipo_arq in self.arquivos_escolhidos:
            self.count_arq += 1
            if tipo_arq.split(".")[-1] == "pdf":
                print(tipo_arq)
                self.bntR_ico["state"] = tk.DISABLED
                self.bntR_JPG["state"] = tk.DISABLED
                self.bntR_pdf["state"] = tk.DISABLED
            else:
                self.bntR_ico["state"] = tk.NORMAL
                self.bntR_JPG["state"] = tk.NORMAL
                self.bntR_pdf["state"] = tk.NORMAL
        if self.arquivos_escolhidos != "":
            self.escolheu_arquivos = True

    def caminho(self):
        self.caminho_nome_pasta = fd.askdirectory(initialdir="")
        # print(self.caminho_nome_pasta)
        if self.caminho_nome_pasta != "":
            self.salva_arquivos = True


    def convert(self):

        if self.escolheu_arquivos and self.salva_arquivos:

            valor_arqs = 100 / self.count_arq
            progresso_atual = 0
            progress = tk.DoubleVar()
            progress.set(0)

            barra_de_progresso = Progressbar(janela, length=200, style='black.Horizontal.TProgressbar', variable=progress)
            barra_de_progresso.grid(column=0, row=0)

            if self.radio_valor.get() == 1:
                tip = "jpeg"
            elif self.radio_valor.get() == 2:
                tip = "png"
            elif self.radio_valor.get() == 3:
                tip = "jpg"
            elif self.radio_valor.get() == 4:
                tip = "ico"
            elif self.radio_valor.get() == 5:
                tip = "pdf"

            poppler_path = r"poppler-22.04.0\Library\bin"
            for caminho in self.arquivos_escolhidos:

                arquivo = caminho.split("/")[-1]
                tipo = arquivo.split(".")[-1]

                if tipo == "pdf":
                    
                    pages = convert_from_path(pdf_path=caminho ,poppler_path=poppler_path)
                    nnumer = 0
                    for page in pages:
                        nnumer += 1
                        # print(page)
                        #nome da imagem
                        arquivo = re.sub("pdf", "", arquivo) #Remoção de caracteres
                        img_name = (arquivo + tip)

                        #imagem = page.convert("RGB")


                        page.save(self.caminho_nome_pasta + "\\" + str(nnumer) + img_name, tip)


                        #imagem.save(self.caminho_nome_pasta+ "\\" + arquivo.replace(tipo, tip))
                        progresso_atual += valor_arqs
                        progress.set(progresso_atual)
                        barra_de_progresso.update_idletasks()

                else:
                    progresso_atual += valor_arqs
                    progress.set(progresso_atual)
                    barra_de_progresso.update_idletasks()
                    imagem = Image.open(caminho).convert("RGB")

                    if self.radio_valor.get() == 4:
                        tipo = arquivo.split(".")[0]
                        logo = Image.open(caminho)
                
                        logo.save(self.caminho_nome_pasta + "\\"  +tipo + ".ico",format='ico')

                    else:
                        imagem.save(self.caminho_nome_pasta+ "\\" + arquivo.replace(tipo, tip))


            messagebox.showinfo("Aviso", "Processo Finalizado")
            barra_de_progresso.destroy()
        else:
            if self.escolheu_arquivos == False and self.salva_arquivos == False:
                messagebox.showerror("Aviso", "Escolha os Arquivos e a pasta para salvar os arquivos")
            elif self.escolheu_arquivos == False and self.salva_arquivos:
                messagebox.showerror("Aviso", "Escolha os Arquivos")
            elif self.escolheu_arquivos and self.salva_arquivos == False:
                messagebox.showerror("Aviso", "Escolha a pasta para salvar os arquivos")
            

janela = tk.Tk()
Tela(janela)
janela.mainloop()
















"""


from PIL import Image
import os


tipo = "ico"


lista_arquivos = os.listdir("Imagens")

for arquivo in lista_arquivos:
    # abrir arquivo
    imagem = Image.open(f"imagens/{arquivo}").convert("RGB")

    if tipo == "ico":

        logo = Image.open(f"C:\\Users\\carlos.ceac\\Desktop\\Python\\Transforma tipos de imagem\\Imagens\\{arquivo}")
 
        logo.save("C:\\Users\\carlos.ceac\\Desktop\\Python\\Transforma tipos de imagem\\Final\\novo.ico",format='ICO')

    else:
        # salvar o arquivo com outro formato
        imagem.save(f'Final/{arquivo.replace("png", "pdf")}')


"""
