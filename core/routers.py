# core/routers.py (ou accounts/routers.py)
class TccRouter:
    """
    Roteia tabelas legadas (do banco tccjava) para o MySQL
    e novas tabelas para o SQLite (default)
    """
    legacy_tables = {
        'pessoa', 'usuario', 'medico', 
        'clinica', 'horarios', 'consulta'
    }

    def db_for_read(self, model, **hints):
        if model._meta.db_table in self.legacy_tables:
            return 'tcc_db'  # Usa o MySQL para tabelas existentes
        return None  # Usa o banco default (SQLite) para outras

    def db_for_write(self, model, **hints):
        if model._meta.db_table in self.legacy_tables:
            return 'tcc_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'tcc_db':
            return False  # Nunca migra para o banco legado
        return True  # Migra normalmente para o SQLite