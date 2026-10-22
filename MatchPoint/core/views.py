from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import IntegrityError, transaction

from .models import PerfilUsuario


@login_required
def editar_usuario(request):
    usuario = request.user

    perfil, criado = PerfilUsuario.objects.get_or_create(
        usuario=usuario
    )

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip()
        foto = request.POST.get("foto", "").strip()
        senha = request.POST.get("senha", "")

        if not nome or not email:
            messages.error(request, "Preencha o nome e o e-mail.")
        elif User.objects.filter(email=email).exclude(pk=usuario.pk).exists():
            messages.error(request, "Este e-mail já está em uso.")
        else:
            partes_nome = nome.split(maxsplit=1)

            usuario.first_name = partes_nome[0]
            usuario.last_name = partes_nome[1] if len(partes_nome) > 1 else ""
            usuario.email = email
            usuario.save()

            perfil.foto = foto
            perfil.save()

            if senha:
                usuario.set_password(senha)
                usuario.save()
                update_session_auth_hash(request, usuario)

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("editar_usuario")

    return render(
        request,
        "editar_usuario.html",
        {
            "usuario": usuario,
            "foto": perfil.foto,
        },
    )



def login_usuario(request):
    erro = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")

        try:
            usuario_email = User.objects.get(email=email)
        except User.DoesNotExist:
            usuario_email = None

        if usuario_email:
            usuario = authenticate(
                request,
                username=usuario_email.username,
                password=senha,
            )

            if usuario is not None:
                login(request, usuario)
                return redirect("home")

        erro = "E-mail ou senha incorretos."

    return render(request, "login.html", {"erro": erro})


    
def cadastro_usuario(request):
    erro = ""

    if request.method == "POST":
        nome = request.POST.get("nome", "").strip()
        email = request.POST.get("email", "").strip().lower()
        senha = request.POST.get("senha", "")
        confirmar_senha = request.POST.get("confirmar_senha", "")

        if not nome or not email or not senha:
            erro = "Preencha todos os campos."
        elif senha != confirmar_senha:
            erro = "As senhas não coincidem."
        elif User.objects.filter(email__iexact=email).exists():
            erro = "Este e-mail já está cadastrado."
        else:
            partes_nome = nome.split(maxsplit=1)

            try:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        username=email,
                        email=email,
                        password=senha,
                        first_name=partes_nome[0],
                        last_name=partes_nome[1] if len(partes_nome) > 1 else "",
                    )

                    PerfilUsuario.objects.create(usuario=usuario)

                login(request, usuario)
                return redirect("home")

            except IntegrityError:
                erro = "Não foi possível criar a conta. Tente novamente."

    return render(request, "cadastro.html", {"erro": erro})

def home(request):
    return render(request, "FigmaTela.html")

@login_required
def lista_de_usuarios(request):
    usuarios = User.objects.all().order_by("first_name")

    return render(
        request,
        "lista_de_usuarios.html",
        {"usuarios": usuarios},
    )


@login_required
def remover_usuario(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("home")

@login_required
def remover_usuario(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("home")

    return render(request, "remover_usuario.html")
    @login_required
def encontrar_parceiros(request):
    '''
    Esta função busca os jogadores cadastrados no banco de dados.
    Ela utiliza a página encontrar_parceiros.html para exibir os jogadores.
    Se o formulário de busca for enviado, mostra apenas os jogadores
    cujo nome contém o texto pesquisado.
    '''
    if request.method == 'GET':
        parceiros = User.objects.all()
        contexto = {
            'parceiros': parceiros,
        }
    else:
        search_query = request.POST.get('search')
        parceiros = User.objects.filter(first_name__icontains=search_query)
        contexto = {
            'search_query': search_query,   # o texto pesquisado
            'parceiros': parceiros,         # os resultados da pesquisa
        }
    return render(request, 'encontrar_parceiros.html', contexto)
    @login_required
def agendar_quadras(request):
    '''
    Esta função exibe as quadras disponíveis para agendamento.
    Por enquanto os dados são de exemplo, porque ainda não existe
    uma tabela de quadras no banco de dados.
    Ela utiliza a página agendar_quadras.html para exibir as quadras.
    '''
    quadras = [
        {
            'nome': 'Rede do Posto 9',
            'esporte': 'Vôlei de praia',
            'detalhes': 'Dupla · 2 de 4 vagas · Todos os níveis',
            'horario': 'Hoje · 17:00',
        },
        {
            'nome': 'Quadra de Areia Copacabana',
            'esporte': 'Beach tennis',
            'detalhes': 'Dupla · 1 de 2 vagas · Intermediário',
            'horario': 'Amanhã · 08:00',
        },
        {
            'nome': 'Arena Leblon',
            'esporte': 'Vôlei de praia',
            'detalhes': '4x4 · 3 de 8 vagas · Iniciante',
            'horario': 'Sáb · 09:30',
        },
        {
            'nome': 'Quadra de Saibro 3',
            'esporte': 'Tênis',
            'detalhes': 'Individual · 1 de 2 vagas · Intermediário',
            'horario': 'Dom · 10:00',
        },
        {
            'nome': 'Arena Central',
            'esporte': 'Futsal',
            'detalhes': '5x5 · 7 de 10 vagas · Todos os níveis',
            'horario': 'Sáb · 20:00',
        },
    ]
    contexto = {
        'quadras': quadras,
    }
    return render(request, 'agendar_quadras.html', contexto)