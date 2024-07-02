import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        self._listYear = self._model.get_anni()
        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._listShape = self._model.get_forme()
        for f in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(f))

    def handle_graph(self, e):
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value
        if anno is not None and forma is not None:
            self._view.txt_result.controls.clear()
            self._view.update_page()
            self._model.crea_grafo(anno, forma)
            num_nodi = self._model.num_nodi()
            num_archi = self._model.num_archi()
            self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {num_nodi}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero archi: {num_archi}"))
            nodi = self._model.get_peso_nodi()
            for c, v in nodi.items():
                self._view.txt_result.controls.append(ft.Text(f"Nodo {c.id}, somma pesi su archi = {v}"))
            self._view.update_page()

        else:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare tutti e due i campi. "))
            self._view.update_page()

    def handle_path(self, e):
        costo, lista = self._model.get_ciclo_max()
        lista_archi = self._model.get_archi(lista)
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {costo}"))
        for n in lista_archi:
            self._view.txtOut2.controls.append(ft.Text(f"{n[0]} --> {n[1]} Peso: {n[2]} Distanza: {n[3]}"))
        self._view.update_page()
