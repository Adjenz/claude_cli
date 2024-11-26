#!/usr/bin/env python3
import os
import sys
import anthropic
from dotenv import load_dotenv
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from pathlib import Path
import stat

# Configuration de Rich pour un affichage amélioré
console = Console()

def get_env_path():
    """Retourne le chemin du fichier .env"""
    return Path(__file__).parent / '.env'

def save_api_key(api_key):
    """Sauvegarde la clé API de manière sécurisée"""
    env_path = get_env_path()
    with open(env_path, 'w') as f:
        f.write(f"ANTHROPIC_API_KEY={api_key}")
    # Set file permissions to 600 (read/write for owner only)
    os.chmod(env_path, stat.S_IRUSR | stat.S_IWUSR)

def setup_client():
    """Configure le client Anthropic avec gestion de la clé API"""
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        console.print(Panel("[yellow]Clé API Anthropic non trouvée.[/yellow]"))
        console.print("Vous pouvez la trouver sur : [link]https://console.anthropic.com/settings/keys[/link]")
        api_key = Prompt.ask("Veuillez entrer votre clé API")
        
        if not api_key:
            console.print("[red]Error:[/red] Une clé API est requise pour utiliser Claude")
            sys.exit(1)
            
        save_api_key(api_key)
        console.print("[green]Clé API sauvegardée avec succès![/green]")
    
    return anthropic.Anthropic(api_key=api_key)

def get_multiline_input():
    """Gère la saisie multi-ligne avec support de commandes spéciales"""
    console.print("\n[green]Vous :[/green]")
    lines = []
    while True:
        try:
            line = input("  ")  # Ajoute une indentation pour le texte
            if line.strip() == "/quit":
                return None
            if line.strip() == "///":
                text = '\n\n'.join(lines)
                if text.strip():
                    console.print("\n[dim]--- Message soumis, en attente de la réponse de Claude... ---[/dim]")
                return text
            lines.append(line)
        except EOFError:
            text = '\n\n'.join(lines)
            if text.strip():
                console.print("\n[dim]--- Message soumis, en attente de la réponse de Claude... ---[/dim]")
            return text
        except KeyboardInterrupt:
            return None

def format_response(text):
    """Formate la réponse de Claude en Markdown"""
    return Markdown(text)

@click.command()
@click.option('--model', default="claude-3-opus-20240229", help="Modèle Claude à utiliser")
@click.option('--max-tokens', default=1024, help="Nombre maximum de tokens pour la réponse")
@click.option('--system', help="Message système pour initialiser la conversation")
def chat_with_claude(model, max_tokens, system):
    """Interface en ligne de commande pour discuter avec Claude"""
    try:
        client = setup_client()
        
        console.print(Panel.fit(
            "[green]Bienvenue dans Claude CLI![/green]\n"
            "- Écrivez votre message sur plusieurs lignes\n"
            "- Utilisez '///' sur une nouvelle ligne pour envoyer\n"
            "- Utilisez '/quit' pour quitter\n"
            "- Ctrl+D reste disponible comme alternative à '///'"
        ))
        
        # Initialize conversation
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        
        while True:
            # Get user input
            user_input = get_multiline_input()
            
            # Check for exit command
            if user_input is None:
                console.print("\n[green]Au revoir ![/green]")
                break
            
            if not user_input.strip():
                continue
            
            try:
                # Send message to Claude
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    messages=[
                        *messages,
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # Print Claude's response
                console.print("\n[blue]Claude:[/blue]")
                console.print(format_response(response.content[0].text))
                
                # Add the exchange to messages history
                messages.extend([
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": response.content[0].text}
                ])
                
            except anthropic.APIError as e:
                console.print(f"\n[red]Erreur API:[/red] {str(e)}")
            except Exception as e:
                console.print(f"\n[red]Erreur inattendue:[/red] {str(e)}")
    
    except KeyboardInterrupt:
        console.print("\n[green]Au revoir ![/green]")
        sys.exit(0)

if __name__ == "__main__":
    chat_with_claude()
