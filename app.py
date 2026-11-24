import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class RateConversionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion Calculator")
        self.resize(1240, 390)
        self.setMinimumSize(1140, 360)

        self._updating = False

        self._init_widgets()
        self._apply_styles()
        self._build_layout()
        self._connect_signals()
        self._sync_from_left_and_recalc()

    def _make_edit(self, text: str, width: int, editable: bool = False, align_right: bool = True) -> QLineEdit:
        line = QLineEdit(text)
        line.setFixedWidth(width)
        line.setAlignment(Qt.AlignRight | Qt.AlignVCenter if align_right else Qt.AlignLeft | Qt.AlignVCenter)
        line.setReadOnly(not editable)
        line.setProperty("editableField", editable)
        return line

    def _make_label(self, text: str, role: str = "symbol") -> QLabel:
        lbl = QLabel(text)
        lbl.setProperty("role", role)
        return lbl

    def _init_widgets(self):
        # Top conversion bar
        self.curr1_edit = self._make_edit("USD", 130, editable=True, align_right=False)
        self.rate1_fixed_edit = self._make_edit("1", 105, editable=False, align_right=True)
        self.curr2_edit = self._make_edit("PHP", 130, editable=True, align_right=False)
        self.rate2_top_edit = self._make_edit("60", 105, editable=True, align_right=True)

        self.swap_btn = QPushButton("Swap")
        self.reset_btn = QPushButton("Reset")
        self.swap_btn.setCursor(Qt.PointingHandCursor)
        self.reset_btn.setCursor(Qt.PointingHandCursor)

        # Left column (Currency 1)
        self.hdr_curr1_edit = self._make_edit("USD", 120, editable=False, align_right=False)
        self.fixed1_1_edit = self._make_edit("1", 120, editable=False, align_right=True)
        self.hour_rate1_edit = self._make_edit("9", 100, editable=True, align_right=True)
        self.out1_hour_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.per_hour1_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.hrs1_edit = self._make_edit("8", 100, editable=True, align_right=True)
        self.out1_day_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.per_day1_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.days1_edit = self._make_edit("5", 100, editable=True, align_right=True)
        self.out1_week_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.bimonth1_left_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.two1_bimonth_edit = self._make_edit("2", 100, editable=False, align_right=True)
        self.out1_bimonth_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.month1_left_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.two1_month_edit = self._make_edit("2", 100, editable=False, align_right=True)
        self.out1_month_edit = self._make_edit("", 120, editable=False, align_right=True)

        # Right column (Currency 2)
        self.hdr_curr2_edit = self._make_edit("PHP", 120, editable=False, align_right=False)
        self.fixed2_1_edit = self._make_edit("1", 120, editable=False, align_right=True)
        self.hour_rate2_edit = self._make_edit("540", 100, editable=True, align_right=True)
        self.out2_hour_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.per_hour2_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.hrs2_edit = self._make_edit("8", 100, editable=True, align_right=True)
        self.out2_day_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.per_day2_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.days2_edit = self._make_edit("5", 100, editable=True, align_right=True)
        self.out2_week_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.bimonth2_left_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.two2_bimonth_edit = self._make_edit("2", 100, editable=False, align_right=True)
        self.out2_bimonth_edit = self._make_edit("", 120, editable=False, align_right=True)

        self.month2_left_edit = self._make_edit("", 120, editable=False, align_right=True)
        self.two2_month_edit = self._make_edit("2", 100, editable=False, align_right=True)
        self.out2_month_edit = self._make_edit("", 120, editable=False, align_right=True)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #18181b;
                color: #f4f4f5;
                font-family: "Consolas", "Segoe UI", monospace;
                font-size: 13px;
            }
            QFrame#card {
                background-color: #202024;
                border: 1px solid #2e2e36;
                border-radius: 6px;
            }
            QLineEdit[editableField="true"] {
                background-color: #2c2c32;
                color: #ffffff;
                border: 1px solid #3f6fa6;
                border-radius: 3px;
                padding: 4px 6px;
                selection-background-color: #2563eb;
            }
            QLineEdit[editableField="true"]:focus {
                background-color: #34343c;
                border: 1px solid #60a5fa;
            }
            QLineEdit[editableField="false"] {
                background-color: #1c1c20;
                color: #d4d4d8;
                border: 1px solid #2e2e36;
                border-radius: 3px;
                padding: 4px 6px;
                selection-background-color: #3f3f46;
            }
            QLabel[role="conversion"] {
                color: #7dd3fc;
                font-family: "Segoe UI", sans-serif;
                font-weight: 600;
                font-size: 13px;
            }
            QLabel[role="header"] {
                color: #6ee7b7;
                font-family: "Segoe UI", sans-serif;
                font-weight: 600;
                font-size: 13px;
            }
            QLabel[role="period"] {
                color: #7dd3fc;
            }
            QLabel[role="symbol"] {
                color: #a1a1aa;
            }
            QPushButton {
                background-color: #27272a;
                color: #f4f4f5;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 5px 12px;
                font-family: "Segoe UI", sans-serif;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3f3f46;
            }
            QPushButton:pressed {
                background-color: #52525b;
            }
            """
        )

    def _build_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 14, 16, 14)
        main_layout.setSpacing(12)

        # Top card
        top_card = QFrame()
        top_card.setObjectName("card")
        top_layout = QHBoxLayout(top_card)
        top_layout.setContentsMargins(14, 10, 14, 10)
        top_layout.setSpacing(8)

        top_layout.addWidget(self.curr1_edit)
        top_layout.addWidget(self.rate1_fixed_edit)
        top_layout.addSpacing(4)
        top_layout.addWidget(self._make_label("Conversion", role="conversion"))
        top_layout.addSpacing(4)
        top_layout.addWidget(self.curr2_edit)
        top_layout.addWidget(self.rate2_top_edit)
        top_layout.addStretch()
        top_layout.addWidget(self.swap_btn)
        top_layout.addWidget(self.reset_btn)

        main_layout.addWidget(top_card)

        # Bottom two columns
        cols_layout = QHBoxLayout()
        cols_layout.setSpacing(14)

        left_card = self._build_column_card(
            hdr_edit=self.hdr_curr1_edit,
            rows=[
                (self.fixed1_1_edit, self.hour_rate1_edit, self.out1_hour_edit, "per hour"),
                (self.per_hour1_edit, self.hrs1_edit, self.out1_day_edit, "per day"),
                (self.per_day1_edit, self.days1_edit, self.out1_week_edit, "per week"),
                (self.bimonth1_left_edit, self.two1_bimonth_edit, self.out1_bimonth_edit, "per bi month"),
                (self.month1_left_edit, self.two1_month_edit, self.out1_month_edit, "per month"),
            ],
        )

        right_card = self._build_column_card(
            hdr_edit=self.hdr_curr2_edit,
            rows=[
                (self.fixed2_1_edit, self.hour_rate2_edit, self.out2_hour_edit, "per hour"),
                (self.per_hour2_edit, self.hrs2_edit, self.out2_day_edit, "per day"),
                (self.per_day2_edit, self.days2_edit, self.out2_week_edit, "per week"),
                (self.bimonth2_left_edit, self.two2_bimonth_edit, self.out2_bimonth_edit, "per bi month"),
                (self.month2_left_edit, self.two2_month_edit, self.out2_month_edit, "per month"),
            ],
        )

        cols_layout.addWidget(left_card)
        cols_layout.addWidget(right_card)
        main_layout.addLayout(cols_layout)

    def _build_column_card(self, hdr_edit: QLineEdit, rows: list) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 12, 14, 12)
        card_layout.setSpacing(8)

        hdr_row = QHBoxLayout()
        hdr_row.setSpacing(8)
        hdr_row.addWidget(hdr_edit)
        hdr_row.addWidget(self._make_label("Rate", role="header"))
        hdr_row.addStretch()
        card_layout.addLayout(hdr_row)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)

        for r_idx, (left_box, right_box, out_box, period_text) in enumerate(rows):
            grid.addWidget(left_box, r_idx, 0)
            grid.addWidget(self._make_label("*", role="symbol"), r_idx, 1, Qt.AlignCenter)
            grid.addWidget(right_box, r_idx, 2)
            grid.addWidget(self._make_label("=", role="symbol"), r_idx, 3, Qt.AlignCenter)
            grid.addWidget(out_box, r_idx, 4)
            grid.addWidget(self._make_label(period_text, role="period"), r_idx, 5, Qt.AlignLeft)

        card_layout.addLayout(grid)
        card_layout.addStretch()
        return card

    def _connect_signals(self):
        self.curr1_edit.textChanged.connect(lambda _t: self._on_change("names"))
        self.curr2_edit.textChanged.connect(lambda _t: self._on_change("names"))
        self.rate2_top_edit.textChanged.connect(lambda _t: self._on_change("top_conv"))
        self.hour_rate1_edit.textChanged.connect(lambda _t: self._on_change("left_rate"))
        self.hour_rate2_edit.textChanged.connect(lambda _t: self._on_change("right_rate"))

        self.hrs1_edit.textChanged.connect(lambda _t: self._on_change("hrs1"))
        self.hrs2_edit.textChanged.connect(lambda _t: self._on_change("hrs2"))
        self.days1_edit.textChanged.connect(lambda _t: self._on_change("days1"))
        self.days2_edit.textChanged.connect(lambda _t: self._on_change("days2"))

        self.swap_btn.clicked.connect(self.swap_currencies)
        self.reset_btn.clicked.connect(self.reset_defaults)

    def swap_currencies(self):
        c1 = self.curr1_edit.text()
        c2 = self.curr2_edit.text()
        r1 = self.hour_rate1_edit.text()
        r2 = self.hour_rate2_edit.text()

        self._updating = True
        try:
            self.curr1_edit.setText(c2)
            self.curr2_edit.setText(c1)
            self.hour_rate1_edit.setText(r2)
            self.hour_rate2_edit.setText(r1)
        finally:
            self._updating = False
        self.recalculate()

    def reset_defaults(self):
        self._updating = True
        try:
            self.curr1_edit.setText("USD")
            self.rate1_fixed_edit.setText("1")
            self.curr2_edit.setText("PHP")
            self.rate2_top_edit.setText("60")
            self.hour_rate1_edit.setText("9")
            self.hrs1_edit.setText("8")
            self.days1_edit.setText("5")
            self.hrs2_edit.setText("8")
            self.days2_edit.setText("5")
        finally:
            self._updating = False
        self._sync_from_left_and_recalc()

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

    def _get_conversion_factor(self):
        top1 = self._parse_float(self.rate1_fixed_edit.text())
        top2 = self._parse_float(self.rate2_top_edit.text())
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
                r1 = self._parse_float(self.hour_rate1_edit.text())
                if r1 is not None and conv is not None:
                    self.hour_rate2_edit.setText(self._raw_num(r1 * conv))
            elif source == "right_rate":
                r2 = self._parse_float(self.hour_rate2_edit.text())
                if r2 is not None and conv is not None and conv != 0:
                    self.hour_rate1_edit.setText(self._raw_num(r2 / conv))
            elif source == "hrs1":
                self.hrs2_edit.setText(self.hrs1_edit.text())
            elif source == "hrs2":
                self.hrs1_edit.setText(self.hrs2_edit.text())
            elif source == "days1":
                self.days2_edit.setText(self.days1_edit.text())
            elif source == "days2":
                self.days1_edit.setText(self.days2_edit.text())
        finally:
            self._updating = False

        self.recalculate()

    def _sync_from_left_and_recalc(self):
        self._on_change("left_rate")

    def recalculate(self):
        c1 = self.curr1_edit.text().strip() or "USD"
        c2 = self.curr2_edit.text().strip() or "PHP"

        self.hdr_curr1_edit.setText(c1)
        self.hdr_curr2_edit.setText(c2)

        self.rate1_fixed_edit.setText("1")
        self.fixed1_1_edit.setText("1")
        self.fixed2_1_edit.setText("1")
        self.two1_bimonth_edit.setText("2")
        self.two1_month_edit.setText("2")
        self.two2_bimonth_edit.setText("2")
        self.two2_month_edit.setText("2")

        r1 = self._parse_float(self.hour_rate1_edit.text())
        r2 = self._parse_float(self.hour_rate2_edit.text())
        hrs = self._parse_float(self.hrs1_edit.text())
        days = self._parse_float(self.days1_edit.text())

        self._update_column(
            rate=r1,
            hrs=hrs,
            days=days,
            out_hour=self.out1_hour_edit,
            per_hour_ro=self.per_hour1_edit,
            out_day=self.out1_day_edit,
            per_day_ro=self.per_day1_edit,
            out_week=self.out1_week_edit,
            bimonth_left=self.bimonth1_left_edit,
            out_bimonth=self.out1_bimonth_edit,
            month_left=self.month1_left_edit,
            out_month=self.out1_month_edit,
        )

        self._update_column(
            rate=r2,
            hrs=hrs,
            days=days,
            out_hour=self.out2_hour_edit,
            per_hour_ro=self.per_hour2_edit,
            out_day=self.out2_day_edit,
            per_day_ro=self.per_day2_edit,
            out_week=self.out2_week_edit,
            bimonth_left=self.bimonth2_left_edit,
            out_bimonth=self.out2_bimonth_edit,
            month_left=self.month2_left_edit,
            out_month=self.out2_month_edit,
        )

    def _update_column(
        self,
        rate,
        hrs,
        days,
        out_hour: QLineEdit,
        per_hour_ro: QLineEdit,
        out_day: QLineEdit,
        per_day_ro: QLineEdit,
        out_week: QLineEdit,
        bimonth_left: QLineEdit,
        out_bimonth: QLineEdit,
        month_left: QLineEdit,
        out_month: QLineEdit,
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

        out_hour.setText(per_hour_str)
        per_hour_ro.setText(per_hour_str)
        out_day.setText(per_day_str)
        per_day_ro.setText(per_day_str)
        out_week.setText(per_week_str)

        bimonth_left.setText(per_week_str)
        out_bimonth.setText(per_bimonth_str)

        month_left.setText(per_bimonth_str)
        out_month.setText(per_month_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RateConversionApp()
    window.show()
    sys.exit(app.exec())
