# Welcome to Salt & Light

A full-stack web application built with Vue.js frontend and Django backend.

## Table of Contents

- [Project Setup](#project-setup)
- [Environment Setup](#environment-setup)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Development](#development)
- [Git Hooks](#git-hooks)

## Project Setup

### Environment Setup

The project uses environment variables for configuration. Here's how to set it up:

1. Development:

   - Copy `.env.local.example` to `.env.local`
   - Modify values as needed for local development
   - `.env.local` is gitignored and should not be committed

2. Production:
   - `.env.production` contains production defaults
   - This file is committed to version control
   - Values can be overridden in production environment

## Backend Setup

### Prerequisites

- Python 3.x
- pip

### Installation

1. Access the repository on VS Code
2. Right click the `Backend/` folder within our repository and select "open in integrated terminal"
3. Type `pip` to see if it is installed
4. If not follow the install instructions
5. Run the command `pip install -r ./requirements.txt`
6. Run the command `python3 manage.py runserver`

## Frontend Setup

### Prerequisites

- Node.js
- npm

### Installation

```bash
cd Frontend
npm install
```

### Development

```bash
# Compiles and hot-reloads for development
npm run serve

# Compiles and minifies for production
npm run build

# Lints and fixes files
npm run lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Git Hooks

Githooks are awesome! They keep the code nice and clean and your QA process short
and sweet. Hooks run before things like commit and push to keep you from forgetting
things that are really easy to forget.

To use them, it's as easy as running `git config core.hooksPath .githooks` after
you've pulled the latest changes of course. :)

Since most everyone in this project is using VSCode, you should be able to do this
in the VSCode git config menu if needed.

Current hooks that exist:

1. a pre-push hook to prevent accidental push to main and lint your code before sending
   off to github
