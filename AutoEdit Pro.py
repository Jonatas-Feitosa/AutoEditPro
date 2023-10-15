import os
import glob
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageFilter, ImageTk #pip install pillow

def cortar_imagem(img,proporcao=3/4):

    largura, altura = img.size

    if largura / altura > 3 / 4:
        nova_largura = int(altura * 3 / 4)
        nova_altura = altura
    else:
        nova_largura = largura
        nova_altura = int(largura * 4 / 3)

    # Calcula as coordenadas de corte para centrar a imagem
    esquerda = (largura - nova_largura) // 2
    superior = (altura - nova_altura) // 2
    direita = esquerda + nova_largura
    inferior = superior + nova_altura

    # Realiza o corte
    img = img.crop((esquerda, superior, direita, inferior))
    return img

def desfocar_imagem(img,raio=50):
    img = img.filter(ImageFilter.GaussianBlur(raio))
    return img
    
def colar_imagem(fundo, img):

    if img.size[0] < img.size[1]:
        altura = fundo.size[1]
        largura = int(fundo.size[0] * fundo.size[1] / img.size[1])
        img = img.resize((largura,altura), resample = Image.LANCZOS)

        pos_horizontal = (fundo.size[0] - img.size[0])//2

        fundo.paste(img, (pos_horizontal, 0), img)

        return fundo
    else:
        largura = fundo.size[0]
        altura = int(fundo.size[1] * fundo.size[0] / img.size[0])
        img = img.resize((largura,altura), resample = Image.LANCZOS)

        pos_vertical = (fundo.size[1] - img.size[1])//2

        fundo.paste(img, (0, pos_vertical), img)
        return fundo

# Função para limitar o tamanho da imagem a 1MB
def limit_image_size(image, max_size_mb):
    image.save(image.filename, optimize=True)

def selecionar_pasta():
    global pasta_imagens
    pasta_imagens = filedialog.askdirectory()
    folder_label.config(text=pasta_imagens)

def processar_imagem():
    contador = 0
    imgs_text = ""
    for imagem in glob.glob(os.path.join(pasta_imagens, "*")):
        contador +=1
        
        if not os.path.exists("Saida"):
            os.makedirs("Saida")

        if imagem.lower().endswith(('.png', '.jpeg', '.gif', '.bmp','jpg')):
            caminho_completo = os.path.join(pasta_imagens, imagem)
            img = Image.open(caminho_completo).convert("RGBA")

            fundo = cortar_imagem(img)
            fundo = desfocar_imagem(fundo)
            img = colar_imagem(fundo,img)

            # Limitar o tamanho da imagem a 1MB
            #limit_image_size(image, max_size_mb=1)

            # Salvar a imagem
            img = img.convert("RGB")
            img.save(r'Saida/' + str(contador) + "-min.jpeg", "JPEG")
            imgs_text += "Salvo: " + str(contador) + "-min.jpg\n"
            imgs_label.config(text=imgs_text)
            img.close()
    print("Finalizado")

# Cria a janela principal
root = Tk()
root.title("AutoEdit Pro")
root.geometry("450x350")
# Botão para selecionar uma pasta com as imagens
browse_button = Button(root, text="Selecionar Pasta", command=selecionar_pasta)
browse_button.pack(pady=10)

# Rótulo para exibir a pasta selecionada
folder_label = Label(root, text="")
folder_label.pack()

imgs_label = Label(root,text="")
imgs_label.pack()

#img = Image.open("teste.jpg")
# Converte a imagem para uma instância da classe PhotoImage
#photo = ImageTk.PhotoImage(img)

#canvas = Canvas(root, height=img.size, width=200)
#canvas.create_image(0, 0, image=photo)
#canvas.pack(side = TOP, expand=True, fill=BOTH)

# Botão para iniciar o processamento
process_button = Button(root, text="Processar Imagens", command=processar_imagem)
process_button.pack(pady=10)

# Rótulo de status
status_label = Label(root, text="")
status_label.pack()

if __name__ == "__main__":
    root.mainloop()