# Claude CLI

Une interface en ligne de commande moderne pour interagir avec Claude via l'API Anthropic.

## Installation

1. Clonez ce dépôt :
```bash
git clone <votre-repo>
cd CLaude
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Rendez le script exécutable :
```bash
chmod +x claude_cli.py
```

2. Lancez le script :
```bash
./claude_cli.py [OPTIONS]
```

Options disponibles :
- `--model` : Modèle Claude à utiliser (défaut: claude-3-opus-20240229)
- `--max-tokens` : Nombre maximum de tokens pour la réponse (défaut: 1024)
- `--system` : Message système pour initialiser la conversation

Lors de la première utilisation, le script vous demandera votre clé API Anthropic.
Vous pouvez la trouver sur : https://console.anthropic.com/settings/keys

La clé sera stockée de manière sécurisée dans un fichier .env.

## Interface de conversation

- Les messages que vous écrivez apparaissent après "Vous :" en vert
- Les réponses de Claude apparaissent après "Claude :" en bleu
- Le texte est automatiquement indenté pour une meilleure lisibilité
- Les réponses sont formatées en Markdown pour une meilleure présentation

## Commandes disponibles

- `/quit` : Quitter l'application
- `///` : Envoyer le message (à taper sur une nouvelle ligne)
- Ctrl+D : Alternative à '///' pour envoyer le message
- Ctrl+C : Interrompre proprement l'application

## Fonctionnalités

- Interface en ligne de commande moderne et colorée
- Support des messages sur plusieurs lignes avec double espacement
- Formatage Markdown des réponses
- Stockage sécurisé de la clé API
- Historique de la conversation maintenu pendant la session
- Gestion des erreurs et des interruptions
- Options de configuration via arguments en ligne de commande

## Exemples d'utilisation

1. Conversation simple :
```bash
./claude_cli.py
```

2. Avec un message système personnalisé :
```bash
./claude_cli.py --system "Tu es un expert en administration système Linux"
```

3. Avec un modèle différent et plus de tokens :
```bash
./claude_cli.py --model claude-3-sonnet-20240229 --max-tokens 2048
