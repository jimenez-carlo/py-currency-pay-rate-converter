import tkinter as tk


class RateConversionApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Conversion Calculator")
        self.root.geometry("1240x380")
        self.root.minsize(1140, 350)
        self.root.configure(bg="#18181b")

        self._updating = False

        # Palette
        self.bg_app = "#18181b"
        self.bg_card = "#202024"
        self.bg_edit = "#2c2c32"
        self.bg_edit_focus = "#34343c"
        self.bg_ro = "#1c1c20"
        self.border_ro = "#2e2e36"
        self.border_edit = "#3f6fa6"
        self.border_focus = "#60a5fa"
        self.fg_primary = "#f4f4f5"
        self.fg_secondary = "#a1a1aa"
        self.fg_accent = "#7dd3fc"
        self.fg_header = "#6ee7b7"

        # Top bar & editable rate variables
        self.curr1_var = tk.StringVar(value="USD")
        self.rate1_fixed_var = tk.StringVar(value="1")
        self.curr2_var = tk.StringVar(value="PHP")
        self.rate2_top_var = tk.StringVar(value="60")

        # Editable rate fields on the "per hour" rows
        self.hour_rate1_var = tk.StringVar(value="9")
        self.hour_rate2_var = tk.StringVar(value="540")

        # Editable hrs and days
        self.hrs1_var = tk.StringVar(value="8")
        self.days1_var = tk.StringVar(value="5")
        self.hrs2_var = tk.StringVar(value="8")
        self.days2_var = tk.StringVar(value="5")

        # Fixed multiplier "2" for bi month and month
        self.two_1_bimonth_var = tk.StringVar(value="2")
        self.two_1_month_var = tk.StringVar(value="2")
        self.two_2_bimonth_var = tk.StringVar(value="2")
        self.two_2_month_var = tk.StringVar(value="2")

        # Read-only entry variables (Left / Currency 1)
        self.hdr_curr1_var = tk.StringVar()
        self.fixed1_1_var = tk.StringVar(value="1")
        self.out1_hour_var = tk.StringVar()

        self.per_hour1_ro_var = tk.StringVar()
        self.out1_day_var = tk.StringVar()

        self.per_day1_ro_var = tk.StringVar()
        self.out1_week_var = tk.StringVar()

        self.bimonth1_left_var = tk.StringVar()
        self.out1_bimonth_var = tk.StringVar()

        self.month1_left_var = tk.StringVar()
        self.out1_month_var = tk.StringVar()

        # Read-only entry variables (Right / Currency 2)
        self.hdr_curr2_var = tk.StringVar()
        self.fixed2_1_var = tk.StringVar(value="1")
        self.out2_hour_var = tk.StringVar()

        self.per_hour2_ro_var = tk.StringVar()
        self.out2_day_var = tk.StringVar()

        self.per_day2_ro_var = tk.StringVar()
        self.out2_week_var = tk.StringVar()

        self.bimonth2_left_var = tk.StringVar()
        self.out2_bimonth_var = tk.StringVar()

        self.month2_left_var = tk.StringVar()
        self.out2_month_var = tk.StringVar()

        self._build_ui()
        self._bind_traces()
        self._sync_from_left_and_recalc()

    def _entry(self, parent, var, width=14, editable=False, justify="right"):
        entry = tk.Entry(
            parent,
            textvariable=var,
            width=width,
            font=("Consolas", 10),
            justify=justify,
            relief="flat",
            bd=1,
            highlightthickness=1,
        )

        if editable:
            entry.configure(
                bg=self.bg_edit,
                fg=self.fg_primary,
                insertbackground=self.fg_primary,
                highlightbackground=self.border_edit,
                highlightcolor=self.border_focus,
                state="normal",
            )
            entry.bind(
                "<FocusIn>",
                lambda _e, w=entry: w.configure(bg=self.bg_edit_focus),
            )
            entry.bind(
                "<FocusOut>",
                lambda _e, w=entry: w.configure(bg=self.bg_edit),
            )
        else:
            entry.configure(
                bg=self.bg_ro,
                fg="#d4d4d8",
                readonlybackground=self.bg_ro,
                highlightbackground=self.border_ro,
                highlightcolor=self.border_ro,
                state="readonly",
            )

        return entry

    def _text_label(self, parent, text, fg=None, anchor="w", bg=None, font=("Consolas", 10)):
        return tk.Label(
            parent,
            text=text,
            bg=bg or self.bg_card,
            fg=fg or self.fg_primary,
            font=font,
            anchor=anchor,
        )

    def _action_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#27272a",
            fg=self.fg_primary,
            activebackground="#3f3f46",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=10,
            pady=4,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )

    def _build_ui(self):
        root_frame = tk.Frame(self.root, bg=self.bg_app, padx=16, pady=14)
        root_frame.pack(fill="both", expand=True)

        # Top Conversion Card
        top_card = tk.Frame(
            root_frame,
            bg=self.bg_card,
            padx=14,
            pady=10,
            highlightbackground=self.border_ro,
            highlightthickness=1,
        )
        top_card.pack(fill="x", pady=(0, 12))

        self._entry(top_card, self.curr1_var, width=16, editable=True, justify="left").pack(
            side="left"
        )
        self._entry(top_card, self.rate1_fixed_var, width=12, editable=False, justify="right").pack(
            side="left", padx=(6, 8)
        )
        self._text_label(
            top_card, "Conversion", fg=self.fg_accent, font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=6)
        self._entry(top_card, self.curr2_var, width=16, editable=True, justify="left").pack(
            side="left", padx=(8, 6)
        )
        self._entry(top_card, self.rate2_top_var, width=12, editable=True, justify="right").pack(
            side="left"
        )

        # Utility buttons on the right of top bar
        self._action_button(top_card, "Reset", self.reset_defaults).pack(side="right", padx=(6, 0))
        self._action_button(top_card, "Swap", self.swap_currencies).pack(side="right")

        # Two aligned column cards
        cols = tk.Frame(root_frame, bg=self.bg_app)
        cols.pack(fill="both", expand=True)

        left_card = tk.Frame(
            cols,
            bg=self.bg_card,
            padx=14,
            pady=12,
            highlightbackground=self.border_ro,
            highlightthickness=1,
        )
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_card = tk.Frame(
            cols,
            bg=self.bg_card,
            padx=14,
            pady=12,
            highlightbackground=self.border_ro,
            highlightthickness=1,
        )
        right_card.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self._build_side(
            parent=left_card,
            hdr_curr_var=self.hdr_curr1_var,
            fixed1_var=self.fixed1_1_var,
            hour_rate_edit_var=self.hour_rate1_var,
            out_hour_var=self.out1_hour_var,
            per_hour_ro_var=self.per_hour1_ro_var,
            hrs_edit_var=self.hrs1_var,
            out_day_var=self.out1_day_var,
            per_day_ro_var=self.per_day1_ro_var,
            days_edit_var=self.days1_var,
            out_week_var=self.out1_week_var,
            bimonth_left_var=self.bimonth1_left_var,
            two_bimonth_var=self.two_1_bimonth_var,
            out_bimonth_var=self.out1_bimonth_var,
            month_left_var=self.month1_left_var,
            two_month_var=self.two_1_month_var,
            out_month_var=self.out1_month_var,
        )

        self._build_side(
            parent=right_card,
            hdr_curr_var=self.hdr_curr2_var,
            fixed1_var=self.fixed2_1_var,
            hour_rate_edit_var=self.hour_rate2_var,
            out_hour_var=self.out2_hour_var,
            per_hour_ro_var=self.per_hour2_ro_var,
            hrs_edit_var=self.hrs2_var,
            out_day_var=self.out2_day_var,
            per_day_ro_var=self.per_day2_ro_var,
            days_edit_var=self.days2_var,
            out_week_var=self.out2_week_var,
            bimonth_left_var=self.bimonth2_left_var,
            two_bimonth_var=self.two_2_bimonth_var,
            out_bimonth_var=self.out2_bimonth_var,
            month_left_var=self.month2_left_var,
            two_month_var=self.two_2_month_var,
            out_month_var=self.out2_month_var,
        )

    def _build_side(
        self,
        parent,
        hdr_curr_var,
        fixed1_var,
        hour_rate_edit_var,
        out_hour_var,
        per_hour_ro_var,
        hrs_edit_var,
        out_day_var,
        per_day_ro_var,
        days_edit_var,
        out_week_var,
        bimonth_left_var,
        two_bimonth_var,
        out_bimonth_var,
        month_left_var,
        two_month_var,
        out_month_var,
    ):
        hdr_frame = tk.Frame(parent, bg=self.bg_card)
        hdr_frame.grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 8))
        self._entry(hdr_frame, hdr_curr_var, width=14, editable=False, justify="left").pack(
            side="left"
        )
        self._text_label(
            hdr_frame, "  Rate", fg=self.fg_header, font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        rows_spec = [
            (
                self._entry(parent, fixed1_var, width=14, editable=False, justify="right"),
                self._entry(parent, hour_rate_edit_var, width=12, editable=True, justify="right"),
                self._entry(parent, out_hour_var, width=14, editable=False, justify="right"),
                "per hour",
            ),
            (
                self._entry(parent, per_hour_ro_var, width=14, editable=False, justify="right"),
                self._entry(parent, hrs_edit_var, width=12, editable=True, justify="right"),
                self._entry(parent, out_day_var, width=14, editable=False, justify="right"),
                "per day",
            ),
            (
                self._entry(parent, per_day_ro_var, width=14, editable=False, justify="right"),
                self._entry(parent, days_edit_var, width=12, editable=True, justify="right"),
                self._entry(parent, out_week_var, width=14, editable=False, justify="right"),
                "per week",
            ),
            (
                self._entry(parent, bimonth_left_var, width=14, editable=False, justify="right"),
                self._entry(parent, two_bimonth_var, width=12, editable=False, justify="right"),
                self._entry(parent, out_bimonth_var, width=14, editable=False, justify="right"),
                "per bi month",
            ),
            (
                self._entry(parent, month_left_var, width=14, editable=False, justify="right"),
                self._entry(parent, two_month_var, width=12, editable=False, justify="right"),
                self._entry(parent, out_month_var, width=14, editable=False, justify="right"),
                "per month",
            ),
        ]

        for row_idx, (left_entry, right_entry, out_entry, period_text) in enumerate(
            rows_spec, start=1
        ):
            left_entry.grid(row=row_idx, column=0, padx=(0, 6), pady=3, sticky="e")
            self._text_label(parent, "*", fg=self.fg_secondary, anchor="center").grid(
                row=row_idx, column=1, padx=4, pady=3
            )
            right_entry.grid(row=row_idx, column=2, padx=(6, 8), pady=3, sticky="e")
            self._text_label(parent, "=", fg=self.fg_secondary, anchor="center").grid(
                row=row_idx, column=3, padx=4, pady=3
            )
            out_entry.grid(row=row_idx, column=4, padx=(8, 10), pady=3, sticky="e")
            self._text_label(parent, period_text, fg=self.fg_accent, anchor="w").grid(
                row=row_idx, column=5, pady=3, sticky="w"
            )

    def swap_currencies(self):
        c1 = self.curr1_var.get()
        c2 = self.curr2_var.get()
        r1 = self.hour_rate1_var.get()
        r2 = self.hour_rate2_var.get()

        self._updating = True
        try:
            self.curr1_var.set(c2)
            self.curr2_var.set(c1)
            self.hour_rate1_var.set(r2)
            self.hour_rate2_var.set(r1)
        finally:
            self._updating = False
        self.recalculate()

    def reset_defaults(self):
        self._updating = True
        try:
            self.curr1_var.set("USD")
            self.rate1_fixed_var.set("1")
            self.curr2_var.set("PHP")
            self.rate2_top_var.set("60")
            self.hour_rate1_var.set("9")
            self.hrs1_var.set("8")
            self.days1_var.set("5")
            self.hrs2_var.set("8")
            self.days2_var.set("5")
        finally:
            self._updating = False
        self._sync_from_left_and_recalc()

    def _bind_traces(self):
        self.rate2_top_var.trace_add("write", lambda *_: self._on_change("top_conv"))
        self.hour_rate1_var.trace_add("write", lambda *_: self._on_change("left_rate"))
        self.hour_rate2_var.trace_add("write", lambda *_: self._on_change("right_rate"))

        self.hrs1_var.trace_add("write", lambda *_: self._on_change("hrs1"))
        self.hrs2_var.trace_add("write", lambda *_: self._on_change("hrs2"))
        self.days1_var.trace_add("write", lambda *_: self._on_change("days1"))
        self.days2_var.trace_add("write", lambda *_: self._on_change("days2"))

        for var in (self.curr1_var, self.curr2_var):
            var.trace_add("write", lambda *_: self._on_change("names"))

    def _get_conversion_factor(self):
        top1 = self._parse_float(self.rate1_fixed_var.get())
        top2 = self._parse_float(self.rate2_top_var.get())
        if top1 is None or top1 == 0 or top2 is None:
            return None
        return top2 / top1

    def _on_change(self, source: str):
        if self._updating:
            return
        self._updating = True
        try:
            conv = self._get_conversion_factor()

            if source in ("top_conv", "left_rate"):
                r1 = self._parse_float(self.hour_rate1_var.get())
                if r1 is not None and conv is not None:
                    self.hour_rate2_var.set(self._raw_num(r1 * conv))
            elif source == "right_rate":
                r2 = self._parse_float(self.hour_rate2_var.get())
                if r2 is not None and conv is not None and conv != 0:
                    self.hour_rate1_var.set(self._raw_num(r2 / conv))
            elif source == "hrs1":
                self.hrs2_var.set(self.hrs1_var.get())
            elif source == "hrs2":
                self.hrs1_var.set(self.hrs2_var.get())
            elif source == "days1":
                self.days2_var.set(self.days1_var.get())
            elif source == "days2":
                self.days1_var.set(self.days2_var.get())
        finally:
            self._updating = False

        self.recalculate()

    def _sync_from_left_and_recalc(self):
        self._on_change("left_rate")

    @staticmethod
    def _parse_float(raw: str):
        try:
            return float(raw.strip())
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _raw_num(num: float) -> str:
        if num.is_integer():
            return str(int(num))
        return f"{num:.6f}".rstrip("0").rstrip(".")

    @staticmethod
    def _fmt(num: float) -> str:
        if num.is_integer():
            return f"{int(num):,}"
        return f"{num:,.2f}"

    def recalculate(self):
        c1 = self.curr1_var.get().strip() or "USD"
        c2 = self.curr2_var.get().strip() or "PHP"

        self.hdr_curr1_var.set(c1)
        self.hdr_curr2_var.set(c2)

        self.rate1_fixed_var.set("1")
        self.fixed1_1_var.set("1")
        self.fixed2_1_var.set("1")
        self.two_1_bimonth_var.set("2")
        self.two_1_month_var.set("2")
        self.two_2_bimonth_var.set("2")
        self.two_2_month_var.set("2")

        r1 = self._parse_float(self.hour_rate1_var.get())
        r2 = self._parse_float(self.hour_rate2_var.get())
        hrs = self._parse_float(self.hrs1_var.get())
        days = self._parse_float(self.days1_var.get())

        self._update_column(
            rate=r1,
            hrs=hrs,
            days=days,
            out_hour_var=self.out1_hour_var,
            per_hour_ro_var=self.per_hour1_ro_var,
            out_day_var=self.out1_day_var,
            per_day_ro_var=self.per_day1_ro_var,
            out_week_var=self.out1_week_var,
            bimonth_left_var=self.bimonth1_left_var,
            out_bimonth_var=self.out1_bimonth_var,
            month_left_var=self.month1_left_var,
            out_month_var=self.out1_month_var,
        )

        self._update_column(
            rate=r2,
            hrs=hrs,
            days=days,
            out_hour_var=self.out2_hour_var,
            per_hour_ro_var=self.per_hour2_ro_var,
            out_day_var=self.out2_day_var,
            per_day_ro_var=self.per_day2_ro_var,
            out_week_var=self.out2_week_var,
            bimonth_left_var=self.bimonth2_left_var,
            out_bimonth_var=self.out2_bimonth_var,
            month_left_var=self.month2_left_var,
            out_month_var=self.out2_month_var,
        )

    def _update_column(
        self,
        rate,
        hrs,
        days,
        out_hour_var,
        per_hour_ro_var,
        out_day_var,
        per_day_ro_var,
        out_week_var,
        bimonth_left_var,
        out_bimonth_var,
        month_left_var,
        out_month_var,
    ):
        per_hour = 1.0 * rate if rate is not None else None
        per_hour_str = self._fmt(per_hour) if per_hour is not None else "?"

        per_day = per_hour * hrs if (per_hour is not None and hrs is not None) else None
        per_day_str = self._fmt(per_day) if per_day is not None else "?"

        per_week = per_day * days if (per_day is not None and days is not None) else None
        per_week_str = self._fmt(per_week) if per_week is not None else "?"

        per_bimonth = per_week * 2.0 if per_week is not None else None
        per_bimonth_str = self._fmt(per_bimonth) if per_bimonth is not None else "?"

        per_month = per_bimonth * 2.0 if per_bimonth is not None else None
        per_month_str = self._fmt(per_month) if per_month is not None else "?"

        out_hour_var.set(per_hour_str)
        per_hour_ro_var.set(per_hour_str)
        out_day_var.set(per_day_str)
        per_day_ro_var.set(per_day_str)
        out_week_var.set(per_week_str)

        bimonth_left_var.set(per_week_str)
        out_bimonth_var.set(per_bimonth_str)

        month_left_var.set(per_bimonth_str)
        out_month_var.set(per_month_str)


if __name__ == "__main__":
    root = tk.Tk()
    app = RateConversionApp(root)
    root.mainloop()
