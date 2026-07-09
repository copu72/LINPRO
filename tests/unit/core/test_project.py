"""Tests para el sistema de proyectos de LINPRO."""

from pathlib import Path

from linpro.core.project import Project, Workspace


class TestProject:
    def test_metadata_correcta(self):
        p = Project(name="Mi Proyecto")
        assert p.metadata.name == "Mi Proyecto"
        assert p.metadata.epsg == 25830
        assert p.metadata.version == "0.1.0"

    def test_set_data_y_get_data(self):
        p = Project("test")
        p.set_data("clave", "valor")
        assert p.get_data("clave") == "valor"

    def test_get_data_default(self):
        p = Project("test")
        assert p.get_data("no_existe", "default") == "default"

    def test_to_dict_incluye_metadata_y_data(self):
        p = Project("test")
        p.set_data("x", 1)
        d = p.to_dict()
        assert d["metadata"]["name"] == "test"
        assert d["data"]["x"] == 1

    def test_from_dict_roundtrip(self):
        original = Project("original")
        original.set_data("a", 100)
        d = original.to_dict()
        copia = Project.from_dict(d)
        assert copia.metadata.name == "original"
        assert copia.get_data("a") == 100

    def test_from_dict_mantiene_loaded(self):
        original = Project("test")
        d = original.to_dict()
        copia = Project.from_dict(d)
        assert copia.state.is_loaded is True

    def test_path_property(self):
        p = Project("test")
        assert p.path is None
        p.path = Path("/ruta/proyecto.linpro")
        assert p.path == Path("/ruta/proyecto.linpro")

    def test_mark_loaded(self):
        p = Project("test")
        assert p.state.is_loaded is False
        p.mark_loaded()
        assert p.state.is_loaded is True
        assert p.state.is_dirty is False

    def test_mark_saved(self):
        p = Project("test")
        p.set_data("x", 1)
        assert p.state.is_dirty is True
        p.mark_saved()
        assert p.state.is_dirty is False

    def test_set_data_marca_dirty(self):
        p = Project("test")
        assert p.state.is_dirty is False
        p.set_data("x", 1)
        assert p.state.is_dirty is True


class TestWorkspace:
    def test_singleton(self):
        a = Workspace.get_instance()
        b = Workspace.get_instance()
        assert a is b

    def test_open_project(self):
        ws = Workspace()
        p = Project("test")
        ws.open_project(p)
        assert ws.current_project is p
        assert p in ws.list_open_projects()

    def test_close_project(self):
        ws = Workspace()
        p = Project("test")
        ws.open_project(p)
        ws.close_project()
        assert ws.current_project is None
        assert p not in ws.list_open_projects()

    def test_open_project_marca_loaded(self):
        ws = Workspace()
        p = Project("test")
        assert p.state.is_loaded is False
        ws.open_project(p)
        assert p.state.is_loaded is True

    def test_current_project_none_inicial(self):
        ws = Workspace()
        assert ws.current_project is None

    def test_list_open_projects_vacio_inicial(self):
        ws = Workspace()
        assert ws.list_open_projects() == []