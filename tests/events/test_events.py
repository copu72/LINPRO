"""Tests para el sistema de eventos de LINPRO."""

import pytest
from datetime import datetime
from linpro.events import EventBus, Event, EventHandler
from linpro.exceptions import EventError


class TestEvent:
    def test_dataclass_name(self):
        evento = Event(name="test.event")
        assert evento.name == "test.event"

    def test_dataclass_data(self):
        evento = Event(name="test.event", data={"clave": "valor"})
        assert evento.data == {"clave": "valor"}

    def test_dataclass_data_vacia_por_defecto(self):
        evento = Event(name="test.event")
        assert evento.data == {}

    def test_dataclass_timestamp_es_datetime(self):
        evento = Event(name="test.event")
        assert isinstance(evento.timestamp, datetime)

    def test_dataclass_timestamp_se_genera_automaticamente(self):
        evento = Event(name="test.event")
        diferencia = datetime.now() - evento.timestamp
        assert diferencia.total_seconds() < 5

    def test_dataclass_timestamp_con_valor(self):
        momento = datetime(2026, 1, 1, 12, 0, 0)
        evento = Event(name="test.event", timestamp=momento)
        assert evento.timestamp == momento


class TestEventBus:
    def setup_method(self):
        EventBus._instance = None

    def test_singleton(self):
        bus1 = EventBus.get_instance()
        bus2 = EventBus.get_instance()
        assert bus1 is bus2

    def test_get_instance_devuelve_siempre_la_misma(self):
        EventBus._instance = None
        bus = EventBus.get_instance()
        assert bus is EventBus.get_instance()

    def test_subscribe_y_publish_ejecuta_handler(self):
        bus = EventBus.get_instance()
        resultados = []

        def handler(event: Event):
            resultados.append(event.data)

        bus.subscribe("test.evento", handler)
        bus.publish(Event(name="test.evento", data={"msg": "hola"}))

        assert len(resultados) == 1
        assert resultados[0] == {"msg": "hola"}

    def test_unsubscribe_evita_ejecucion(self):
        bus = EventBus.get_instance()
        resultados = []

        def handler(event: Event):
            resultados.append(True)

        bus.subscribe("test.evento", handler)
        bus.unsubscribe("test.evento", handler)
        bus.publish(Event(name="test.evento"))

        assert len(resultados) == 0

    def test_suscribir_y_desuscribir_multiple(self):
        bus = EventBus.get_instance()
        resultados_a = []
        resultados_b = []

        def handler_a(event: Event):
            resultados_a.append("a")

        def handler_b(event: Event):
            resultados_b.append("b")

        bus.subscribe("test.multi", handler_a)
        bus.subscribe("test.multi", handler_b)
        bus.publish(Event(name="test.multi"))

        assert len(resultados_a) == 1
        assert len(resultados_b) == 1

        bus.unsubscribe("test.multi", handler_a)
        bus.publish(Event(name="test.multi"))

        assert len(resultados_a) == 1
        assert len(resultados_b) == 2

    def test_clear_elimina_todos_los_handlers(self):
        bus = EventBus.get_instance()
        resultados = []

        def handler(event: Event):
            resultados.append(True)

        bus.subscribe("test.evento", handler)
        bus.clear()
        bus.publish(Event(name="test.evento"))

        assert len(resultados) == 0

    def test_publicar_sin_suscritores_no_lanza_error(self):
        bus = EventBus.get_instance()
        try:
            bus.publish(Event(name="evento.sin.suscritores"))
        except Exception:
            pytest.fail("publish() lanzó excepción sin suscriptores")

    def test_error_en_handler_lanza_event_error(self):
        bus = EventBus.get_instance()

        def handler_que_falla(event: Event):
            raise ValueError("Error interno")

        bus.subscribe("test.fallo", handler_que_falla)

        with pytest.raises(EventError, match="test.fallo"):
            bus.publish(Event(name="test.fallo"))