"""
Jogo dos Trabalhos: interface gráfica para o LW_Environment.

A interface só desenha o estado e repassa as decisões do jogador:
  - clicar em "Aceitar"      -> env.step(trabalho)
  - clicar em "Avançar turno" -> env.step()   (nada a escolher)
  - piloto automático         -> env.step() com env.policy (chooseWork decide)
Toda a dinâmica (aparecer, sumir, concluir) fica em environment.py.
"""
import tkinter as tk
from tkinter import ttk

from environment import LW_Environment

NULL_WORK = [0, 0, 0, 0]


def greedy_policy(state, actions):
    # Retorno esperado por turno: recompensa * chance de concluir (geométrica)
    return max(actions, key=lambda work: work[1] * work[2])


AUTO_DELAY_MS = 700

# Paleta: quadro de despacho em tons de sálvia, tinta esverdeada e marca-texto amarelo
BG = "#DCE4DF"
CARD = "#FAFBFA"
BORDER = "#B7C4BD"
INK = "#1E2B2A"
MUTED = "#587069"
ACCENT = "#0F6B5C"
BUSY = "#FFD76B"
DONE = "#0F6B5C"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_HEAD = ("Georgia", 13, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_SMALL = ("Helvetica", 10)


def make_card(parent, bg=CARD):
    return tk.Frame(parent, bg=bg, highlightbackground=BORDER, highlightthickness=1)


def read_int(var, low, high, default):
    try:
        value = int(var.get())
    except (tk.TclError, ValueError):
        return default
    return max(low, min(high, value))


class LWGame(tk.Tk):
    def __init__(self, n_works=3, goal=10):
        super().__init__()
        self.title("Jogo dos Trabalhos")
        self.configure(bg=BG)
        self.minsize(1020, 640)

        self.n_works = tk.IntVar(value=n_works)
        self.goal = tk.IntVar(value=goal)
        self.auto = tk.BooleanVar(value=False)
        self._after_id = None
        self.turn = 0
        self.total_reward = 0

        self._setup_style()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.new_game()

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=FONT_BODY, padding=(12, 6))
        style.configure("Accent.TButton", background=ACCENT, foreground="white",
                        bordercolor=ACCENT, focuscolor=INK)
        style.map("Accent.TButton",
                  background=[("disabled", BORDER), ("active", "#0B5547")],
                  foreground=[("disabled", "#F2F5F3")])
        style.configure("Score.Horizontal.TProgressbar", troughcolor=CARD,
                        background=ACCENT, bordercolor=BORDER, thickness=16)
        style.configure("Busy.Horizontal.TProgressbar", troughcolor="#F3E6B8",
                        background=INK, bordercolor="#E0C766", thickness=6)
        style.configure("Treeview", font=FONT_SMALL, rowheight=24,
                        background=CARD, fieldbackground=CARD, foreground=INK)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
        style.configure("TCheckbutton", background=BG, foreground=INK, font=FONT_BODY)
        style.configure("TSpinbox", arrowsize=12)

    def _build_ui(self):
        self.columnconfigure(0, weight=3, uniform="col")
        self.columnconfigure(1, weight=2, uniform="col")
        self.rowconfigure(1, weight=1)

        # Cabeçalho: título, pontuação e contadores
        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(14, 6))
        top.columnconfigure(0, weight=1)
        tk.Label(top, text="Jogo dos Trabalhos", font=FONT_TITLE,
                 bg=BG, fg=INK).grid(row=0, column=0, sticky="w")
        self.lbl_stats = tk.Label(top, font=FONT_BODY, bg=BG, fg=MUTED)
        self.lbl_stats.grid(row=0, column=1, sticky="e")

        score_row = tk.Frame(top, bg=BG)
        score_row.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        self.lbl_score = tk.Label(score_row, font=FONT_HEAD, bg=BG, fg=INK, width=16, anchor="w")
        self.lbl_score.pack(side="left")
        self.progress = ttk.Progressbar(score_row, style="Score.Horizontal.TProgressbar",
                                        mode="determinate")
        self.progress.pack(side="left", fill="x", expand=True)

        # Coluna principal: trabalho atual, disponíveis e controles
        main = tk.Frame(self, bg=BG)
        main.grid(row=1, column=0, sticky="nsew", padx=(18, 9), pady=(8, 16))
        main.columnconfigure(0, weight=1)
        main.rowconfigure(3, weight=1)

        tk.Label(main, text="Trabalho atual", font=FONT_HEAD, bg=BG, fg=INK).grid(
            row=0, column=0, sticky="w")
        self.current_card = make_card(main)
        self.current_card.grid(row=1, column=0, sticky="ew", pady=(4, 14))
        self.current_card.columnconfigure(0, weight=1)
        self.lbl_current_title = tk.Label(self.current_card, font=FONT_HEAD, anchor="w")
        self.lbl_current_title.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 0))
        self.lbl_current_info = tk.Label(self.current_card, font=FONT_SMALL,
                                         anchor="w", justify="left")
        self.lbl_current_info.grid(row=1, column=0, sticky="ew", padx=14, pady=(2, 6))
        self.busy_bar = ttk.Progressbar(self.current_card, style="Busy.Horizontal.TProgressbar",
                                        mode="indeterminate")
        self.busy_bar.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))

        tk.Label(main, text="Trabalhos disponíveis", font=FONT_HEAD, bg=BG, fg=INK).grid(
            row=2, column=0, sticky="w")
        self.avail_frame = tk.Frame(main, bg=BG)
        self.avail_frame.grid(row=3, column=0, sticky="nsew", pady=(4, 8))

        self.lbl_banner = tk.Label(main, font=FONT_HEAD, bg=BG, fg=DONE, anchor="w")
        self.lbl_banner.grid(row=4, column=0, sticky="ew", pady=(0, 6))

        controls = tk.Frame(main, bg=BG)
        controls.grid(row=5, column=0, sticky="ew")
        self.btn_wait = ttk.Button(controls, command=self.wait)
        self.btn_wait.pack(side="left")
        ttk.Checkbutton(controls, text="Piloto automático", variable=self.auto,
                        command=self._toggle_auto).pack(side="left", padx=16)
        ttk.Button(controls, text="Reiniciar partida", command=self.restart).pack(side="right")

        # Coluna lateral: catálogo, registro e nova partida
        side = tk.Frame(self, bg=BG)
        side.grid(row=1, column=1, sticky="nsew", padx=(9, 18), pady=(8, 16))
        side.columnconfigure(0, weight=1)
        side.rowconfigure(3, weight=1)

        tk.Label(side, text="Catálogo de trabalhos", font=FONT_HEAD, bg=BG, fg=INK).grid(
            row=0, column=0, sticky="w")
        columns = [("name", "Trabalho", 78), ("cost", "Custo", 46), ("reward", "Rec.", 40),
                   ("finish", "Conclui", 56), ("show", "Surge", 52), ("gone", "Some", 48),
                   ("status", "Situação", 74)]
        self.tree = ttk.Treeview(side, columns=[c[0] for c in columns],
                                 show="headings", height=5, selectmode="none")
        for key, title, width in columns:
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="w" if key in ("name", "status") else "center")
        self.tree.grid(row=1, column=0, sticky="ew", pady=(4, 12))

        tk.Label(side, text="Registro", font=FONT_HEAD, bg=BG, fg=INK).grid(
            row=2, column=0, sticky="w")
        log_frame = make_card(side)
        log_frame.grid(row=3, column=0, sticky="nsew", pady=(4, 12))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        self.log_text = tk.Text(log_frame, font=FONT_SMALL, bg=CARD, fg=INK, wrap="word",
                                relief="flat", state="disabled", height=8, padx=8, pady=6)
        scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll.set)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        self.log_text.tag_configure("gain", foreground=DONE, font=("Helvetica", 10, "bold"))
        self.log_text.tag_configure("pick", foreground=INK, font=("Helvetica", 10, "bold"))
        self.log_text.tag_configure("minor", foreground=MUTED)

        setup = tk.Frame(side, bg=BG)
        setup.grid(row=4, column=0, sticky="ew")
        tk.Label(setup, text="Trabalhos", font=FONT_SMALL, bg=BG, fg=INK).pack(side="left")
        ttk.Spinbox(setup, from_=2, to=5, width=3, textvariable=self.n_works).pack(
            side="left", padx=(6, 14))
        tk.Label(setup, text="Meta de pontos", font=FONT_SMALL, bg=BG, fg=INK).pack(side="left")
        ttk.Spinbox(setup, from_=1, to=20, width=3, textvariable=self.goal).pack(
            side="left", padx=(6, 14))
        ttk.Button(setup, text="Nova partida", command=self.new_game).pack(side="right")

    # ------------------------------------------------------------------
    # Ciclo de partida
    # ------------------------------------------------------------------
    def new_game(self):
        self._stop_auto()
        n = read_int(self.n_works, 2, 5, 3)
        goal = read_int(self.goal, 1, 20, 10)
        self.n_works.set(n)
        self.goal.set(goal)
        self.env = LW_Environment(list(NULL_WORK), [], goal, n_works=n)
        self.env.policy = greedy_policy  # só é usada no piloto automático
        self._build_catalog()
        self._reset_counters()
        self.log(f"Nova partida: {n} trabalhos, meta de {goal} pontos.", "minor")
        self.refresh()

    def restart(self):
        self._stop_auto()
        self.env.reset()
        self._reset_counters()
        self.log("Partida reiniciada com os mesmos trabalhos.", "minor")
        self.refresh()

    def _reset_counters(self):
        self.turn = 0
        self.total_reward = 0
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _stop_auto(self):
        self.auto.set(False)
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None

    def _on_close(self):
        self._stop_auto()
        self.destroy()

    @property
    def finished(self):
        return self.env.isGoal(self.env.state)

    # ------------------------------------------------------------------
    # Ações do jogador
    # ------------------------------------------------------------------
    def accept(self, work):
        if self.finished or self.auto.get():
            return
        self._advance(work)

    def wait(self):
        if self.finished or self.auto.get():
            return
        self._advance(None)

    def _advance(self, action):
        _, r = self.env.step(action)
        self.turn += 1
        self.total_reward += r
        self._log_events()
        self.refresh()

    def _toggle_auto(self):
        if self.auto.get() and self.finished:
            self.auto.set(False)
        elif self.auto.get():
            self._schedule_auto()
        elif self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        self.refresh()

    def _schedule_auto(self):
        self._after_id = self.after(AUTO_DELAY_MS, self._auto_step)

    def _auto_step(self):
        self._after_id = None
        if not self.auto.get() or self.finished:
            return
        self._advance(None)  # chooseWork delega para env.policy
        if self.auto.get() and not self.finished:
            self._schedule_auto()

    # ------------------------------------------------------------------
    # Desenho do estado
    # ------------------------------------------------------------------
    def name(self, work):
        if work == NULL_WORK:
            return "Livre"
        try:
            return f"Trabalho {chr(ord('A') + self.env.works.index(work) - 1)}"
        except ValueError:
            return "Trabalho ?"

    @staticmethod
    def describe(work):
        return (f"Custo {work[0]}, recompensa {work[1]}, conclui {work[2]:.0%} por turno\n"
                f"Surge {work[3]:.0%} por turno, some {work[4]:.0%} por turno")

    def _build_catalog(self):
        self.tree.delete(*self.tree.get_children())
        for i, w in enumerate(self.env.works[1:], start=1):
            self.tree.insert("", "end", iid=str(i), values=(
                self.name(w), w[0], w[1], f"{w[2]:.0%}", f"{w[3]:.0%}", f"{w[4]:.0%}", "-"))

    def refresh(self):
        env = self.env
        current, listed, score = env.state
        goal = env.goal[2]
        idle = current == NULL_WORK
        available = [w for w in listed if w != NULL_WORK]
        finished = self.finished
        manual = not finished and not self.auto.get()

        self.lbl_stats.configure(text=f"Turno {self.turn}     Retorno acumulado {self.total_reward}")
        self.lbl_score.configure(text=f"Pontos {score} de {goal}")
        self.progress.configure(maximum=goal, value=score)

        # Trabalho atual
        color = CARD if idle else BUSY
        self.current_card.configure(bg=color)
        for label in (self.lbl_current_title, self.lbl_current_info):
            label.configure(bg=color, fg=INK)
        if idle:
            self.busy_bar.stop()
            self.busy_bar.grid_remove()
            self.lbl_current_title.configure(text="Ocioso")
            self.lbl_current_info.configure(
                text="Escolha um dos trabalhos abaixo." if available
                else "Nenhum trabalho na lista. Avance o turno e espere um surgir.")
        else:
            self.busy_bar.grid()
            self.busy_bar.start(30)
            self.lbl_current_title.configure(text=self.name(current))
            self.lbl_current_info.configure(text=self.describe(current))

        # Trabalhos disponíveis (só aceitáveis quando ocioso)
        for child in self.avail_frame.winfo_children():
            child.destroy()
        if available:
            for work in available:
                self._work_card(work, enabled=idle and manual)
        else:
            tk.Label(self.avail_frame, text="A lista está vazia.", font=FONT_BODY,
                     bg=BG, fg=MUTED).pack(anchor="w", pady=4)

        # Botão de avanço: só vale quando não há escolha obrigatória
        if idle and not available:
            self.btn_wait.configure(text="Esperar um trabalho")
        else:
            self.btn_wait.configure(text="Avançar turno")
        can_wait = manual and (not idle or not available)
        self.btn_wait.state(["!disabled"] if can_wait else ["disabled"])

        # Catálogo
        for i, w in enumerate(env.works[1:], start=1):
            if w == current:
                status = "Fazendo"
            elif w in available:
                status = "Na lista"
            else:
                status = "-"
            self.tree.set(str(i), "status", status)

        if finished:
            self._stop_auto()
            self.lbl_banner.configure(
                text=f"Meta atingida em {self.turn} turnos. Retorno acumulado: {self.total_reward}.")
        else:
            self.lbl_banner.configure(text="")

    def _work_card(self, work, enabled):
        card = make_card(self.avail_frame)
        card.pack(fill="x", pady=4)
        card.columnconfigure(0, weight=1)
        tk.Label(card, text=self.name(work), font=FONT_HEAD, bg=CARD, fg=INK,
                 anchor="w").grid(row=0, column=0, sticky="w", padx=12, pady=(8, 0))
        tk.Label(card, text=self.describe(work), font=FONT_SMALL, bg=CARD, fg=MUTED,
                 justify="left", anchor="w").grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
        button = ttk.Button(card, text="Aceitar", style="Accent.TButton",
                            command=lambda w=work: self.accept(w))
        button.grid(row=0, column=1, rowspan=2, padx=12)
        if not enabled:
            button.state(["disabled"])

    # ------------------------------------------------------------------
    # Registro de eventos
    # ------------------------------------------------------------------
    def log(self, text, tag=None):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n", tag)
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _log_events(self):
        events = self.env.last_events
        prefix = f"Turno {self.turn}: "
        if not events:
            self.log(prefix + "nada mudou.", "minor")
        for event in events:
            kind, work = event[0], event[1]
            if kind == "picked":
                self.log(prefix + f"{self.name(work)} aceito.", "pick")
            elif kind == "finished":
                self.log(prefix + f"{self.name(work)} concluído, +{event[2]} pontos.", "gain")
            elif kind == "appeared":
                self.log(prefix + f"{self.name(work)} entrou na lista.", "minor")
            elif kind == "disappeared":
                self.log(prefix + f"{self.name(work)} saiu da lista.", "minor")


if __name__ == "__main__":
    LWGame().mainloop()
