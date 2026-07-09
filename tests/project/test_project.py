"""Tests para el sistema de proyectos y workspace de LINPRO."""

import pytest
from datetime import datetime
from linpro.project import Project, ProjectMetadata, ProjectState, Workspace
from linpro.exceptions import ProjectError, WorkspaceError


class TestProjectMetadata:
    def test_dataclass_campos_basicos(self):
        meta = ProjectMetadata(name="Proyecto prueba", author="Carlos")
        assert meta.name == "Proyecto prueba"
        assert meta.author == "Carlos"

    def test_dataclass_valores_por_defecto(self):
        meta = ProjectMetadata(name="test")
        assert meta.description == ""
        assert meta.company == ""
        assert meta.version == "0.1.0"
        assert meta.epsg == 25830
        assert isinstance(meta.created, datetime)
        assert isinstance(meta.modified, datetime)


class TestProjectState:
    def test_valores_iniciales(self):
        estado = ProjectState()
        assert estado.is_dirty is False
        assert estado.is_loaded is False
        assert estado.has_alignment is False
        assert estado.has_analysis is False
        assert estado.has_results is False


class TestProject:
    def test_creacion_con_nombre(self):
        proyecto = Project(name="Mi Proyecto")
        assert proyecto.metadata.name == "Mi Proyecto"
        assert proyecto.state.is_dirty is False
        assert proyecto.state.is_loaded is False
        assert proyecto.path is None

    def test_creacion_sin_nombre(self):
        proyecto = Project()
        assert proyecto.metadata.name == "Sin título"

    def test_set_data_y_get_data(self):
        proyecto = Project()
        proyecto.set_data("linea_base", "VALOR_LINEA")
        assert proyecto.get_data("linea_base") == "VALOR_LINEA"

    def test_set_data_actualiza_modified_y_dirty(self):
        proyecto = Project()
        modified_anterior = proyecto.metadata.modified
        proyecto.set_data("clave", "valor")
        assert proyecto.metadata.modified >= modified_anterior
        assert proyecto.state.is_dirty is True

    def test_get_data_default(self):
        proyecto = Project()
        assert proyecto.get_data("clave_inexistente", "default") == "default"

    def test_get_data_sin_default_devuelve_none(self):
        proyecto = Project()
        assert proyecto.get_data("clave_inexistente") is None

    def test_to_dict_contiene_metadata_y_data(self):
        proyecto = Project(name="test")
        proyecto.set_data("resultados", {"ok": True})
        d = proyecto.to_dict()
        assert d["metadata"]["name"] == "test"
        assert d["data"]["resultados"] == {"ok": True}

    def test_to_dict_metadata_tiene_todos_los_campos(self):
        proyecto = Project(name="completo", )

        proyecto.metadata.description = "Descripción"
        proyecto.metadata.author = "Autor"
        proyecto.metadata.company = "Compañía"
        d = proyecto.to_dict()

        assert d["metadata"]["name"] == "completo"
        assert d["metadata"]["description"] == "Descripción"
        assert d["metadata"]["author"] == "Autor"
        assert d["metadata"]["company"] == "Compañía"
        assert d["metadata"]["version"] == "0.1.0"
        assert d["metadata"]["epsg"] == 25830

    def test_from_dict_roundtrip(self):
        proyecto_original = Project(name="Roundtrip")
        proyecto_original.set_data("puntos", [1, 2, 3])
        proyecto_original.metadata.author = "Carlos"
        proyecto_original.metadata.description = "Prueba de ida y vuelta"

        datos = proyecto_original.to_dict()
        proyecto_cargado = Project.from_dict(datos)

        assert proyecto_cargado.metadata.name == "Roundtrip"
        assert proyecto_cargado.metadata.author == "Carlos"
        assert proyecto_cargado.metadata.description == "Prueba de ida y vuelta"
        assert proyecto_cargado.get_data("puntos") == [1, 2, 3]
        assert proyecto_cargado.state.is_loaded is True

    def test_from_dict_sin_metadata(self):
        proyecto = Project.from_dict({"data": {"clave": "valor"}})
        assert proyecto.metadata.name == "Sin título"
        assert proyecto.get_data("clave") == "valor"

    def test_mark_loaded(self):
        proyecto = Project()
        proyecto.set_data("x", 1)
        proyecto.mark_loaded()
        assert proyecto.state.is_loaded is True
        assert proyecto.state.is_dirty is False

    def test_mark_saved(self):
        proyecto = Project()
        proyecto.set_data("x", 1)
        proyecto.mark_saved()
        assert proyecto.state.is_dirty is False

    def test_path_setter(self):
        from pathlib import Path
        proyecto = Project()
        ruta = Path("/tmp/proyecto.linpro")
        proyecto.path = ruta
        assert proyecto.path == ruta

    def test_repr(self):
        proyecto = Project(name="Test")
        assert "Test" in repr(proyecto)


class TestWorkspace:
    def setup_method(self):
        Workspace._instance = None

    def test_singleton(self):
        ws1 = Workspace.get_instance()
        ws2 = Workspace.get_instance()
        assert ws1 is ws2

    def test_current_project_inicial(self):
        ws = Workspace.get_instance()
        assert ws.current_project is None

    def test_open_project_establece_current(self):
        ws = Workspace.get_instance()
        proyecto = Project(name="Abierto")
        ws.open_project(proyecto)
        assert ws.current_project is proyecto
        assert proyecto.state.is_loaded is True

    def test_open_project_agrega_a_lista(self):
        ws = Workspace.get_instance()
        p1 = Project(name="P1")
        p2 = Project(name="P2")
        ws.open_project(p1)
        ws.open_project(p2)
        assert len(ws.list_open_projects()) == 2

    def test_open_project_no_duplica(self):
        ws = Workspace.get_instance()
        proyecto = Project(name="Unico")
        ws.open_project(proyecto)
        ws.open_project(proyecto)
        assert len(ws.list_open_projects()) == 1

    def test_close_project_limpia_current(self):
        ws = Workspace.get_instance()
        proyecto = Project(name="Cerrar")
        ws.open_project(proyecto)
        ws.close_project()
        assert ws.current_project is None

    def test_close_project_remueve_de_lista(self):
        ws = Workspace.get_instance()
        proyecto = Project(name="Remover")
        ws.open_project(proyecto)
        ws.close_project()
        assert len(ws.list_open_projects()) == 0

    def test_open_close_roundtrip(self):
        ws = Workspace.get_instance()
        proyecto = Project(name="Ciclo")
        ws.open_project(proyecto)
        assert ws.current_project is proyecto
        ws.close_project()
        assert ws.current_project is None
        assert proyecto not in ws.list_open_projects()