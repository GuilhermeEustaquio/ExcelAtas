#!/usr/bin/env python3
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from programa_completo.main import process_pdf, save_xlsx
from programa_completo.renomear_pdf_ata import extrair_numero_ata_e_ug, nome_ata, renomear_pdf

BG = "#f3f5f7"
PRIMARY = "#00796b"
ACCENT = "#cddc39"
CARD = "#ffffff"


class ExcelAtasApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ExcelAtas Desktop")
        self.geometry("820x420")
        self.configure(bg=BG)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 8), font=("Segoe UI", 10, "bold"))

        header = tk.Frame(self, bg=PRIMARY, padx=16, pady=14)
        header.pack(fill="x")
        tk.Label(
            header,
            text="ExcelAtas",
            bg=PRIMARY,
            fg="white",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Interface local para processar e renomear atas em PDF",
            bg=PRIMARY,
            fg="#d7fffb",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=16, pady=16)

        tab_extract = tk.Frame(notebook, bg=CARD)
        tab_rename = tk.Frame(notebook, bg=CARD)

        notebook.add(tab_extract, text="Gerar XLSX")
        notebook.add(tab_rename, text="Renomear PDF")

        self._build_extract_tab(tab_extract)
        self._build_rename_tab(tab_rename)

    def _build_extract_tab(self, parent: tk.Frame) -> None:
        self.extract_pdf = tk.StringVar()
        self.extract_out = tk.StringVar(value="Relatorio.xlsx")

        tk.Label(parent, text="PDF de entrada", bg=CARD).pack(anchor="w", padx=16, pady=(16, 4))
        self._path_row(parent, self.extract_pdf, filetypes=[("PDF", "*.pdf")]).pack(fill="x", padx=16)

        tk.Label(parent, text="Arquivo XLSX de saída", bg=CARD).pack(anchor="w", padx=16, pady=(16, 4))
        tk.Entry(parent, textvariable=self.extract_out).pack(fill="x", padx=16)

        tk.Button(
            parent,
            text="Gerar Planilha",
            bg=PRIMARY,
            fg="white",
            activebackground=ACCENT,
            relief="flat",
            command=self.handle_extract,
            padx=12,
            pady=8,
        ).pack(anchor="w", padx=16, pady=20)

    def _build_rename_tab(self, parent: tk.Frame) -> None:
        self.rename_pdf = tk.StringVar()

        tk.Label(parent, text="PDF para renomear", bg=CARD).pack(anchor="w", padx=16, pady=(16, 4))
        self._path_row(parent, self.rename_pdf, filetypes=[("PDF", "*.pdf")]).pack(fill="x", padx=16)

        tk.Button(
            parent,
            text="Sugerir Nome",
            bg=PRIMARY,
            fg="white",
            activebackground=ACCENT,
            relief="flat",
            command=self.handle_preview_name,
            padx=12,
            pady=8,
        ).pack(anchor="w", padx=16, pady=(20, 8))

        tk.Button(
            parent,
            text="Renomear Arquivo",
            bg="#0d9488",
            fg="white",
            relief="flat",
            command=self.handle_rename,
            padx=12,
            pady=8,
        ).pack(anchor="w", padx=16)

    def _path_row(self, parent: tk.Frame, var: tk.StringVar, filetypes: list[tuple[str, str]]) -> tk.Frame:
        row = tk.Frame(parent, bg=CARD)
        tk.Entry(row, textvariable=var).pack(side="left", fill="x", expand=True)

        def browse() -> None:
            selected = filedialog.askopenfilename(filetypes=filetypes)
            if selected:
                var.set(selected)

        tk.Button(row, text="Selecionar", command=browse, relief="flat", bg="#e5e7eb").pack(side="left", padx=6)
        return row

    def handle_extract(self) -> None:
        pdf_path = Path(self.extract_pdf.get().strip())
        out_path = Path(self.extract_out.get().strip())

        if not pdf_path.exists():
            messagebox.showerror("Erro", "Selecione um PDF válido.")
            return

        try:
            rows = process_pdf(pdf_path)
            if not rows:
                messagebox.showwarning("Aviso", "Nenhum item CRO/2 foi encontrado no PDF.")
                return

            save_xlsx(rows, out_path)
            messagebox.showinfo("Sucesso", f"Planilha gerada em:\n{out_path.resolve()}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Erro", str(exc))

    def handle_preview_name(self) -> None:
        pdf_path = Path(self.rename_pdf.get().strip())
        if not pdf_path.exists():
            messagebox.showerror("Erro", "Selecione um PDF válido.")
            return

        try:
            numero_ata, ug = extrair_numero_ata_e_ug(pdf_path)
            if not numero_ata or not ug:
                messagebox.showwarning("Aviso", "Não foi possível localizar número da ata/UG no arquivo.")
                return

            messagebox.showinfo("Nome sugerido", nome_ata(numero_ata, ug))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Erro", str(exc))

    def handle_rename(self) -> None:
        pdf_path = Path(self.rename_pdf.get().strip())
        if not pdf_path.exists():
            messagebox.showerror("Erro", "Selecione um PDF válido.")
            return

        try:
            novo = renomear_pdf(pdf_path)
            self.rename_pdf.set(str(novo))
            messagebox.showinfo("Sucesso", f"Arquivo renomeado para:\n{novo.name}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Erro", str(exc))


if __name__ == "__main__":
    app = ExcelAtasApp()
    app.mainloop()
