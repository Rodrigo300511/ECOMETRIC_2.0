"""
database.py - Gerenciamento de Conexão com Banco de Dados

Módulo responsável pela conexão com o banco SQLite e
validação de integridade das conexões.
"""

import sqlite3
import os


def conectar():
    """
    Estabelece conexão com banco de dados SQLite.
    
    Returns:
        sqlite3.Connection: Conexão ativa com o banco de dados
    
    Note:
        Cria o arquivo 'ecometric.db' no diretório atual se não existir
    """
    db_path = os.path.join(os.path.dirname(__file__), '..', 'ecometric.db')
    return sqlite3.connect(db_path)


def fechar_conexao(conn):
    """
    Fecha conexão com banco de dados de forma segura.
    
    Args:
        conn (sqlite3.Connection): Conexão a ser fechada
    """
    if conn:
        conn.close()