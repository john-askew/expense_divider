import time, datetime, statistics, os
from datetime import datetime

integrantes = []
cuentas = []
descripcion = {}
archivos = []


def new_group():
    global integrantes, cuentas, descripcion

    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    txt = open(f"{timestamp}.txt", "x")
    txt.close()


    try:
        cantidad_integrantes = int(input("How many people are in the group? "))

        while cantidad_integrantes != 0:
            nombre = input("What is the name of the person? ")
            integrantes.append(nombre.capitalize())
            cuentas.append(0)
            descripcion[nombre] = []
            cantidad_integrantes = cantidad_integrantes - 1

            graba = open(f"{timestamp}.txt", "a")
            graba.write(nombre.capitalize() +";"+ str(cuentas[integrantes.index(nombre)]) +";"+ str(descripcion[nombre]) + "\n")
            graba.close()

            print("Name added")
            time.sleep(1)
            print("----------------------------")
    except:
        print("Something went wrong")


def look_back():                            # Show the .txt files in the directory
    i = 1

    print("----------------------------")
    print("This is the list of expenses by date: ")
    contenido = os.listdir()
    
    for archivo in contenido:
        if archivo.endswith(".txt"):
            archivos.append(archivo)

    for archivo in archivos:
        archivo = archivo[0:-4]
        archivo =  datetime.fromtimestamp(int(archivo))
        print("Option", i, ":", archivo)
        i = i + 1
    print("----------------------------")

    print("Which of the options above is the one you want to see?")
    opcion = int(input("Write the number: "))

    time.sleep(1)

    return opcion

    
def see_file(opcion):                             # Read the .txt file selected and put the information in a list
    global integrantes, cuentas, descripcion, archivos

    txt_to_list(archivos[opcion-1])

    print("----------------------------")

    for integrante in integrantes:
        print(integrante, ":", "$", cuentas[integrantes.index(integrante)], "\nResumen: \n", *descripcion[integrante][1:])

    print("----------------------------")

    settlement(integrantes, cuentas)

    return (archivos[opcion-1])
    
    
def add_expense(archivo):                   # Add expenses to the .txt file selected
    global integrantes, cuentas, descripcion, archivos

    txt = open(str(archivo), "r")
    
    txt_to_list(archivo)

    print("Who of this users pay?")
    for integrante in integrantes:
        print(integrante)
    print("----------------------------")
    seleccion = str(input("Write: ").capitalize())

    if seleccion in integrantes:
            
        pago = int(input("How much its cost: "))

        if pago > 0:
            cuentas[integrantes.index(seleccion)] = cuentas[integrantes.index(seleccion)] + pago
            print("Which is the description of the expense?")
            descripcion = str(input())

            graba = open(str(archivo), "a")
            graba.write(seleccion +";"+ str(cuentas[integrantes.index(seleccion)]) +";"+ descripcion + "\n")
            graba.close()

            print("Expense added")
            time.sleep(1)
            
            print("----------------------------")


def settlement(user_list, expenses_list):   # Calculate the total amount of expenses and the amount each user has to pay           
    global integrantes, cuentas

    user_list = integrantes
    expenses_list = cuentas

    x = statistics.mean(cuentas)
    for saldo in cuentas:
        if saldo > x:
            print(f"The user {integrantes[cuentas.index(saldo)]} has a debt of ${round(saldo - x,2)}")
        elif saldo == x:
            print(f"The user {integrantes[cuentas.index(saldo)]} has a balance of ${round(saldo - x, 2)}")
        else:
            print(f"The user {integrantes[cuentas.index(saldo)]} expects to receive ${round(x - saldo, 2)}")


def txt_to_list(archivo):                   # Read the .txt file selected and put the information in a list
    global integrantes, cuentas, descripcion

    txt = open(str(archivo), "r")
    for line in txt:
        x = line.split(";")[0]
        y = line.split(";")[1]
        z = line.split(";")[2]
        if x not in integrantes:
            integrantes.append(x)
            cuentas.append(int(y))
            descripcion[x] = []
            descripcion[x].append(z)    
        else:
            cuentas[integrantes.index(x)] = cuentas[integrantes.index(x)] + int(y)
            descripcion[x].append(z)
    txt.close()
    time.sleep(1)


def modified():                             # Menu to modify the expenses, users and the amount of each user
    global integrantes, cuentas, descripcion

    print("Which of the options above is the one you want to modify?")
    print("1- User from a group")
    print("2- Expense from a group")
    print("3- Group")

    opcion = int(input("Write the number: "))
    if opcion == 1:
        x = look_back()
        z = see_file(x)
        modified_user(z)
    elif opcion == 2:
        x = see_file()
        #modified_expense(x)
    elif opcion == 3:
        x = see_file()
        #modified_group(x)   
    else:
        print("Invalid option")
        time.sleep(1)
        print("----------------------------")


def modified_user(archivo):                 # Modify the user selected
    global integrantes

    txt = open(str(archivo), "r")

    txt_to_list(archivo)

    txt.close()


    print("Which of this user is the one you want to modify?")
    for integrante in integrantes:
        print(integrante)

    print("----------------------------")

    seleccion = str(input("Write: ").capitalize())

    if seleccion in integrantes:
        new_name = str(input("Write the new name: ").capitalize())
        integrantes[integrantes.index(seleccion)] = new_name
        print("User modified")

        search = seleccion
        replace = new_name

        f =  open (str(archivo), "r") 
        data = f.read()
        data = data.replace(search, replace)
        f.close()
        f = open (str(archivo), "w")
        f.write(data)
        f.close()
          

def menu():
    print("----------------------------")
    print("Tell us what you want to do: ")
    print("1 - Start a new group of expense")
    print("2 - Look back at your expenses")
    print("3 - Continue with a group of expenses")
    print("4 - Modified something")
    print("----------------------------")
    seleccion = int(input("Write the number of your choice: "))
    return seleccion

def main(x):
    global archivos

    if x == 1:
        new_group()

    elif x == 2:
        z = look_back()
        see_file(z)   

    elif x == 3:
        y = look_back()
        add_expense(archivos[y-1])

    elif x == 4:
        modified()

    else:
        print("Invalid option")
        time.sleep(1)
        print("----------------------------")




print("Welcome to Expenser Divider!")
while True:
    x = menu()
    main(x)
    print("In 3 secondos you will be redirected to the main menu")
    time.sleep(3)
    integrantes = []
    cuentas = []
    descripcion = {}
    archivos = []