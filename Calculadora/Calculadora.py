import soma
import subtrai
import multiplica
import divide

num1 = float(input("Digite o primeiro número"))
num2 = float(input("Digite o segundo número"))
operador = input("Digite o operador: "))


while operador not in ["+", "-", "*", "x", "/"]:
    print("Operador inválido!")
    operador = input("Digite o operador novamente: ")
    
if operador == "+":
    resultado = soma.somaf(num1, num2)
    
elif operador == "-":
    resultado = subtrai.subtraif(num1, num2)
    
elif operador == "/":
    resultado = divide.dividef(num1, num2)
    
else:
    resultado = multiplica.multiplicaf(num1, num2)
       
print(f"Resultado: {resultado}")



    