import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

api_key = "Enter your API_Key"
custom_font = ("Comic Sans MS", 13, "bold")
custom_font2 = ("Comic Sans MS", 13, "normal")
datalar = {}
weather_image = None

# Tkinter Ayarları :
window = Tk()
window.title("Weather APP")
window.minsize(width=380, height=350)
window.iconbitmap(r"C:\Users\okana\Desktop\PycharmProjects\OpenWeather\images\icon.ico")

# Tkinter Widgets :
# 1. Sütun
hava_durumu_label = Label(text="Hava Durumu : ", font=custom_font, fg="#4289fc")
hava_durumu_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

temp_label = Label(text="Sıcaklık : ", font=custom_font, fg="#4289fc")
temp_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

nem_label = Label(text="Nem : ", font=custom_font, fg="#4289fc")
nem_label.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

ruz_label = Label(text="Rüzgar Hızı : ", font=custom_font, fg="#4289fc")
ruz_label.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

# 2. Sütun
weather_desc_label = Label(text=f"{datalar.get('weather_description')}", font=custom_font2)
weather_desc_label.grid(row=0, column=1, sticky="nsew")

temp_v_label = Label(text=f"{datalar.get('temperature_c')} °C", font=custom_font2)
temp_v_label.grid(row=1, column=1, sticky="nsew")

nem_v_label = Label(text=f"{datalar.get('humidity')} %", font=custom_font2)
nem_v_label.grid(row=2, column=1, sticky="nsew")

ruz_v_label = Label(text=f"{datalar.get('wind_speed')} m/s", font=custom_font2)
ruz_v_label.grid(row=3, column=1, sticky="nsew")

# 3.Sütun
icon_label = Label(bg="light blue")
icon_label.grid(row=0, column=2, rowspan=4, sticky="nsew", padx=5, pady=5)

update_time_label = Label(text="Güncelleme Saati: Bilinmiyor", font=custom_font2, fg="#13ba34")
update_time_label.grid(row=5, column=0, columnspan=3, sticky="nsew")

location_label = Label(text="Konum: Bilinmiyor", font=custom_font2, background="#91755e", fg="white")
location_label.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)


# Enlem ve Boylam verileri alma:
def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            datalar["latitude"] = data["lat"]
            datalar["longitude"] = data["lon"]
            return {
                "latitude": data["lat"],
                "longitude": data["lon"]
            }
        else:
            messagebox.showinfo("Hata", "Konum bilgisi alınamadı!")
            return None
    except Exception as e:
        print("Hata:", e)
        return None


# Hava Durumu verileri alma:
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={datalar.get('latitude')}&lon={datalar.get('longitude')}&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        # Hava durumu verilerini işleyin
        datalar["weather_description"] = data["weather"][0]["description"].title()
        datalar["icon_name"] = data["weather"][0]["icon"]
        datalar["temperature_k"] = data["main"]["temp"]
        datalar["temperature_c"] = round(datalar.get('temperature_k') - 273.15, 2)
        datalar["humidity"] = data["main"]["humidity"]
        datalar["wind_speed"] = data["wind"]["speed"]

    else:
        print("Hava durumu bilgisi alınamadı.")


def get_img():
    try:
        image_url = f"https://openweathermap.org/img/wn/{datalar.get('icon_name')}@2x.png"
        print(image_url)
        response_img = requests.get(image_url)

        # İstek başarılı mı kontrol et
        if response_img.status_code == 200:
            image_data = BytesIO(response_img.content)
            original_image = Image.open(image_data)
            image = ImageTk.PhotoImage(original_image)
            print("Resim başarılı")
            return image
        else:
            print("Görüntü indirme hatası:", response_img.status_code)
            return None
    except Exception as e:
        print("Görüntü işleme hatası:", e)
        return None


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def update_widgets():
    global weather_image

    # 2. Sütun
    weather_desc_label.config(text=f"{datalar.get('weather_description')}", font=custom_font2)
    temp_v_label.config(text=f"{datalar.get('temperature_c')} °C", font=custom_font2)
    nem_v_label.config(text=f"{datalar.get('humidity')} %", font=custom_font2)
    ruz_v_label.config(text=f"{datalar.get('wind_speed')} m/s", font=custom_font2)

    # 3.Sütun
    weather_image = get_img()
    icon_label.config(bg="light blue", image=weather_image)

    # Güncelleme saati etiketini güncelle
    update_time_label.config(text=f"Güncelleme Saati: {get_current_time()}")

    #Konum label günclle
    location_label.config(text=f"Konum : {datalar.get('latitude')} Enlem ve {datalar.get('longitude')} Boylam ")


def update_weather():
    location = get_location()

    if location:
        datalar["latitude"] = location["latitude"]
        datalar["longitude"] = location["longitude"]
        print(f"Enlem: {datalar.get('latitude')}, Boylam: {datalar.get('longitude')}")
        get_weather()
        update_widgets()


update_weather()

# Button widget
update_button = Button(text="Verileri Güncelle", command=update_weather, font=custom_font2)
update_button.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)

window.mainloop()
