import os
import re
from datetime import date, datetime, timedelta

import streamlit as st
from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()

APP_TODAY = date(2026, 3, 24)


# =========================
# NEW: DARK PREMIUM THEME
# =========================
def apply_dark_premium_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #0E1117;
            --card: #1A1C24;
            --card-2: #151821;
            --text: #F5F7FA;
            --muted: #98A2B3;
            --line: rgba(255,255,255,0.08);
            --neon: #22D3EE;
            --neon-2: #8B5CF6;
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(34,211,238,0.10), transparent 24%),
                radial-gradient(circle at top right, rgba(139,92,246,0.12), transparent 28%),
                linear-gradient(180deg, #0E1117 0%, #0B0E14 100%);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(14,17,23,0.65);
        }

        [data-testid="stToolbar"] {
            right: 1rem;
        }

        h1, h2, h3, h4, h5, h6, p, label, div, span {
            color: var(--text);
        }

        .premium-title {
            padding: 18px 22px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(26,28,36,0.96), rgba(20,23,31,0.96));
            border: 1px solid rgba(34,211,238,0.18);
            box-shadow:
                0 0 0 1px rgba(139,92,246,0.06),
                0 12px 40px rgba(0,0,0,0.35),
                inset 0 1px 0 rgba(255,255,255,0.04);
            margin-bottom: 12px;
        }

        .premium-title h1 {
            margin: 0;
            font-size: 32px;
            font-weight: 800;
            letter-spacing: 0.2px;
        }

        .premium-title p {
            margin: 6px 0 0 0;
            color: var(--muted);
            font-size: 14px;
        }

        .premium-chip {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(34,211,238,0.10);
            border: 1px solid rgba(34,211,238,0.24);
            color: #D9FBFF;
            font-size: 12px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(26,28,36,0.95), rgba(20,23,31,0.95));
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 18px;
            padding: 14px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.22);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        [data-testid="stMetricValue"] {
            color: var(--text);
            font-weight: 800;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(255,255,255,0.02);
            padding: 8px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 10px 16px;
            color: var(--muted);
            background: transparent;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(34,211,238,0.18), rgba(139,92,246,0.18));
            color: white !important;
            border: 1px solid rgba(34,211,238,0.22);
        }

        .stButton > button,
        .stDownloadButton > button,
        .stForm button[type="submit"] {
            border-radius: 12px;
            border: 1px solid rgba(34,211,238,0.24);
            background: linear-gradient(135deg, rgba(34,211,238,0.18), rgba(139,92,246,0.18));
            color: white;
            font-weight: 700;
            box-shadow: 0 8px 22px rgba(0,0,0,0.18);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        .stForm button[type="submit"]:hover {
            border-color: rgba(34,211,238,0.45);
            box-shadow: 0 0 0 1px rgba(34,211,238,0.18), 0 10px 28px rgba(0,0,0,0.28);
        }

        .stTextInput > div > div,
        .stTextArea textarea,
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stNumberInput > div > div {
            background-color: #141823 !important;
            color: white !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 10px 32px rgba(0,0,0,0.18);
        }

        [data-testid="stForm"] {
            background: linear-gradient(180deg, rgba(26,28,36,0.95), rgba(20,23,31,0.95));
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 18px;
            padding: 18px;
        }

        [data-testid="stVerticalBlock"] [data-testid="stContainer"] {
            border-radius: 18px;
        }

        hr {
            border-color: rgba(255,255,255,0.06);
        }

        .premium-note {
            color: var(--muted);
            font-size: 13px;
            margin-top: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_premium_header() -> None:
    st.markdown(
        """
        <div class="premium-title">
            <div class="premium-chip">Dark Premium • Neon UI</div>
            <h1>Vanta ERP</h1>
            <p>Управление парком, ремонтами, арендой и аналитикой</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_supabase_client() -> Client | None:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        st.error("Не найдены SUPABASE_URL и/или SUPABASE_KEY в .env")
        return None
    return create_client(url, key)


def fetch_table(client: Client, table_name: str) -> list[dict]:
    try:
        response = client.table(table_name).select("*").execute()
        return response.data or []
    except Exception as error:
        st.error(f"Ошибка при загрузке таблицы '{table_name}': {error}")
        return []


def parse_missing_column(error_text: str) -> str | None:
    patterns = [
        r"column [\w\.]+\.([\w_]+) does not exist",
        r"Could not find the '([\w_]+)' column",
    ]
    for pattern in patterns:
        match = re.search(pattern, error_text)
        if match:
            return match.group(1)
    return None


def insert_repair_ticket(client: Client, payload: dict) -> dict | None:
    attempts = []
    base = payload.copy()
    attempts.append(base.copy())
    if "employee_id" in base:
        mechanic_payload = base.copy()
        mechanic_payload["mechanic_id"] = mechanic_payload.pop("employee_id")
        attempts.append(mechanic_payload)

    for candidate in attempts:
        current = candidate.copy()
        for _ in range(6):
            try:
                response = client.table("repair_tickets").insert(current).execute()
                data = response.data or []
                return data[0] if data else None
            except Exception as error:
                text = str(error)
                missing_column = parse_missing_column(text)
                if missing_column and missing_column in current:
                    del current[missing_column]
                    continue
                if "employee_id" in text and "employee_id" in current:
                    current["mechanic_id"] = current.pop("employee_id")
                    continue
                if "PGRST204" in text or "42703" in text:
                    continue
                raise
    return None


def ensure_work_day(client: Client, employee_id: int) -> None:
    today_iso = APP_TODAY.isoformat()
    payloads = [
        ({"employee_id": employee_id, "date": today_iso}, "employee_id,date"),
        ({"employee_id": employee_id, "work_date": today_iso}, "employee_id,work_date"),
    ]
    for payload, conflict in payloads:
        try:
            client.table("work_days").upsert(payload, on_conflict=conflict).execute()
            return
        except Exception:
            continue


def detect_work_type(mode: str, parts_count: int, comment: str) -> str:
    if mode == "assembly":
        return "assembly"
    if parts_count > 0:
        return "parts"
    if len(comment.strip()) <= 20:
        return "details"
    return "repair"


def normalize_status(value: str | None) -> str:
    raw = str(value or "").strip().lower()
    if raw in {"свободен", "available", "free"}:
        return "Свободен"
    if raw in {"в ремонте", "repair", "maintenance"}:
        return "В ремонте"
    if raw in {"занят", "busy", "rented"}:
        return "Занят"
    if raw in {"в аренде"}:
        return "В аренде"
    if raw in {"на дарксторе"}:
        return "На дарксторе"
    if raw in {"нужна эвакуация"}:
        return "Нужна эвакуация"
    return str(value or "Не указан")


def bike_metrics(bikes: list[dict]) -> tuple[int, int, int]:
    free_count = sum(1 for x in bikes if normalize_status(x.get("status")) == "Свободен")
    repair_count = sum(1 for x in bikes if normalize_status(x.get("status")) == "В ремонте")
    busy_count = sum(1 for x in bikes if normalize_status(x.get("status")) == "Занят")
    return free_count, repair_count, busy_count


def darkstore_number_map(darkstores: list[dict]) -> dict[int, str]:
    result: dict[int, str] = {}
    for ds in darkstores:
        ds_id = ds.get("id")
        if ds_id is None:
            continue
        number = ds.get("number")
        result[ds_id] = str(number) if number is not None else str(ds_id)
    return result


def fetch_bike_history(client: Client, bike_id: int) -> list[dict]:
    try:
        response = (
            client.table("repair_tickets")
            .select("id,created_at,comment,work_type,status")
            .eq("bike_id", bike_id)
            .order("created_at", desc=True)
            .limit(6)
            .execute()
        )
        rows = response.data or []
    except Exception:
        rows = []
    return [
        {
            "Дата": row.get("created_at") or "-",
            "Комментарий": row.get("comment") or "-",
            "Тип работ": row.get("work_type") or "-",
            "Статус заявки": row.get("status") or "-",
        }
        for row in rows
    ]


# =========================
# NEW: BIKE SWAP LOGIC
# =========================
def fetch_bike_by_id(client: Client, bike_id: int) -> dict | None:
    try:
        response = client.table("bikes").select("*").eq("id", bike_id).limit(1).execute()
        rows = response.data or []
        return rows[0] if rows else None
    except Exception as error:
        st.error(f"Ошибка загрузки велосипеда ID={bike_id}: {error}")
        return None


def swap_bikes(client: Client, old_bike_id: int, new_bike_id: int, transfer_plate: bool = True) -> tuple[bool, str]:
    """
    Переносит со старого байка на новый:
    - plate (если transfer_plate=True)
    - current_darkstore_id

    Старому байку ставит:
    - tech_status = 'Ожидает ремонта'

    Дополнительно:
    - старый байк отвязывается от current_darkstore_id
    - если plate переносился, у старого plate обнуляется
    - статус нового байка наследуется от старого, если у старого он есть
    """
    if old_bike_id == new_bike_id:
        return False, "Старый и новый байк не должны совпадать."

    old_bike = fetch_bike_by_id(client, old_bike_id)
    new_bike = fetch_bike_by_id(client, new_bike_id)

    if not old_bike:
        return False, "Старый велосипед не найден."
    if not new_bike:
        return False, "Новый велосипед не найден."

    old_plate = old_bike.get("plate")
    old_darkstore_id = old_bike.get("current_darkstore_id")
    old_status = old_bike.get("status") or "Свободен"

    updates_new = {
        "current_darkstore_id": old_darkstore_id,
        "status": old_status,
    }
    if transfer_plate:
        updates_new["plate"] = old_plate

    updates_old = {
        "tech_status": "Ожидает ремонта",
        "current_darkstore_id": None,
    }
    if transfer_plate:
        updates_old["plate"] = None

    try:
        client.table("bikes").update(updates_new).eq("id", new_bike_id).execute()
        client.table("bikes").update(updates_old).eq("id", old_bike_id).execute()
        return True, "Успешно: замена выполнена. Старый байк отправлен в 'Ожидает ремонта'."
    except Exception as error:
        return False, f"Ошибка замены: {error}"


def status_chip(value: str) -> str:
    if value == "Свободен":
        return "🟢 Свободен"
    if value == "В ремонте":
        return "🔴 В ремонте"
    if value == "Занят":
        return "🟠 Занят"
    if value == "В аренде":
        return "🔵 В аренде"
    if value == "На дарксторе":
        return "🟣 На дарксторе"
    if value == "Нужна эвакуация":
        return "🟡 Нужна эвакуация"
    return f"⚪ {value}"


def render_bikes_tab(client: Client) -> None:
    st.subheader("Велосипеды")
    bikes = fetch_table(client, "bikes")
    darkstores = fetch_table(client, "darkstores")
    ds_number_by_id = darkstore_number_map(darkstores)
    if not bikes:
        st.info("В таблице bikes пока нет данных.")
        return

    awaiting = [b for b in bikes if str(b.get("tech_status") or "").strip() == "Ожидает ремонта"]
    if awaiting:
        st.markdown("### Фокус мастеров: Ожидает ремонта")
        st.dataframe(
            [
                {
                    "Серийный номер": b.get("sn"),
                    "Гос. номер": b.get("plate"),
                    "Даркстор": ds_number_by_id.get(b.get("current_darkstore_id"), "-"),
                    "Статус": normalize_status(b.get("status")),
                    "Тех. состояние": b.get("tech_status") or "-",
                }
                for b in awaiting
            ],
            use_container_width=True,
            hide_index=True,
            height=220,
        )

    c1, c2, c3, c4 = st.columns(4)
    free_count, repair_count, busy_count = bike_metrics(bikes)
    c1.metric("Всего", len(bikes))
    c2.metric("Свободно", free_count)
    c3.metric("В ремонте", repair_count)
    c4.metric("Занято", busy_count)

    f1, f2, f3 = st.columns([2.2, 1.2, 1.2])
    with f1:
        query = st.text_input("Поиск (SN / Гос. номер / IoT)")
    with f2:
        status_values = sorted({normalize_status(x.get("status")) for x in bikes})
        status_filter = st.multiselect("Статус", options=status_values)
    with f3:
        tech_values = sorted({str(x.get("tech_status") or "Не указан") for x in bikes})
        tech_filter = st.multiselect("Тех. состояние", options=tech_values)

    filtered = bikes
    if query.strip():
        q = query.strip().lower()
        filtered = [
            x
            for x in filtered
            if q in str(x.get("sn") or "").lower()
            or q in str(x.get("plate") or "").lower()
            or q in str(x.get("iot") or "").lower()
        ]
    if status_filter:
        filtered = [x for x in filtered if normalize_status(x.get("status")) in status_filter]
    if tech_filter:
        filtered = [x for x in filtered if str(x.get("tech_status") or "Не указан") in tech_filter]

    header = st.columns([1.2, 1, 1, 1, 1, 1.1, 2.2])
    header[0].markdown("**Серийный номер**")
    header[1].markdown("**Статус**")
    header[2].markdown("**Тех. состояние**")
    header[3].markdown("**IoT**")
    header[4].markdown("**Гос. номер**")
    header[5].markdown("**Даркстор**")
    header[6].markdown("**Действия**")
    st.divider()

    for bike in filtered:
        bike_id = bike.get("id")
        if bike_id is None:
            continue
        details_key = f"show_details_{bike_id}"
        edit_key = f"show_edit_{bike_id}"

        row = st.columns([1.2, 1, 1, 1, 1, 1.1, 2.2])
        row[0].write(bike.get("sn") or "-")
        row[1].write(status_chip(normalize_status(bike.get("status"))))
        row[2].write(str(bike.get("tech_status") or "Не указан"))
        row[3].write(str(bike.get("iot") or "-"))
        row[4].write(str(bike.get("plate") or "-"))
        row[5].write(ds_number_by_id.get(bike.get("current_darkstore_id"), "-"))
        with row[6]:
            b1, b2, b3 = st.columns(3)
            if b1.button("Изменить", key=f"edit_btn_{bike_id}"):
                st.session_state[edit_key] = not st.session_state.get(edit_key, False)
            if b2.button("В ремонт", key=f"repair_btn_{bike_id}"):
                st.session_state["repair_bike_id"] = bike_id
                st.success("Байк добавлен в ремонт.")
            if b3.button("Подробнее", key=f"details_btn_{bike_id}"):
                st.session_state[details_key] = not st.session_state.get(details_key, False)

        if st.session_state.get(edit_key, False) or st.session_state.get(details_key, False):
            with st.container(border=True):
                if st.session_state.get(edit_key, False):
                    with st.form(f"bike_edit_form_{bike_id}"):
                        edit_iot = st.text_input("IoT", value=bike.get("iot") or "", key=f"edit_iot_{bike_id}")
                        edit_plate = st.text_input("Гос. номер", value=bike.get("plate") or "", key=f"edit_plate_{bike_id}")
                        edit_status = st.selectbox("Статус", options=["Свободен", "В ремонте", "Занят"])
                        save_bike = st.form_submit_button("Сохранить")
                    if save_bike:
                        try:
                            (
                                client.table("bikes")
                                .update(
                                    {"iot": edit_iot.strip() or None, "plate": edit_plate.strip() or None, "status": edit_status}
                                )
                                .eq("id", bike_id)
                                .execute()
                            )
                            st.success("Успешно сохранено!")
                            st.rerun()
                        except Exception as error:
                            st.error(f"Ошибка сохранения: {error}")

                if st.session_state.get(details_key, False):
                    history_rows = fetch_bike_history(client, bike_id)
                    st.markdown("**История (последние 6 действий):**")
                    if history_rows:
                        st.dataframe(history_rows, use_container_width=True, hide_index=True)
                    else:
                        st.info("История обслуживания пока пустая.")
        st.divider()


def render_repair_tab(client: Client) -> None:
    st.subheader("Цех")

    if "parts_rows" not in st.session_state:
        st.session_state["parts_rows"] = []

    employees = fetch_table(client, "employees")
    bikes = fetch_table(client, "bikes")
    parts = fetch_table(client, "parts")

    employee_map = {
        f"{x.get('name') or x.get('full_name') or 'Сотрудник'} (ID: {x.get('id')})": x.get("id")
        for x in employees
        if x.get("id") is not None
    }
    bike_map = {f"{x.get('sn') or 'Без SN'} (ID: {x.get('id')})": x.get("id") for x in bikes if x.get("id") is not None}
    part_map = {
        f"{x.get('name') or 'Запчасть'} (ID: {x.get('id')})": x.get("id")
        for x in parts
        if x.get("id") is not None
    }

    mode = st.radio("Тип работы", ["Ремонт", "Сборка нового байка"])

    if mode == "Сборка нового байка":
        with st.form("assembly_form"):
            sn = st.text_input("SN")
            iot = st.text_input("IoT")
            plate = st.text_input("Гос. номер")
            assembly_employee_label = st.selectbox(
                "Мастер",
                options=list(employee_map.keys()),
                index=None,
                placeholder="Выберите мастера...",
            )
            assembly_comment = st.text_area("Комментарий")
            submit_assembly = st.form_submit_button("Завершить сборку")
        if submit_assembly:
            employee_id = employee_map.get(assembly_employee_label)
            if not sn.strip() or employee_id is None:
                st.error("Укажите SN и выберите мастера.")
                return
            try:
                bike_resp = (
                    client.table("bikes")
                    .insert({"sn": sn.strip(), "iot": iot.strip() or None, "plate": plate.strip() or None, "status": "Свободен"})
                    .execute()
                )
                bike_data = bike_resp.data or []
                bike_id = bike_data[0].get("id") if bike_data else None
                work_type = detect_work_type("assembly", 0, assembly_comment)
                if bike_id is not None:
                    insert_repair_ticket(
                        client,
                        {
                            "bike_id": bike_id,
                            "employee_id": employee_id,
                            "comment": assembly_comment,
                            "work_type": work_type,
                        },
                    )
                    ensure_work_day(client, employee_id)
                st.success("Успешно: сборка сохранена.")
                st.rerun()
            except Exception as error:
                st.error(f"Ошибка сохранения сборки: {error}")
        return

    st.markdown("### Внутренний ремонт")
    col1, col2 = st.columns(2)
    with col1:
        employee_label = st.selectbox(
            "Мастер",
            options=list(employee_map.keys()),
            index=None,
            placeholder="Выберите мастера...",
        )
    with col2:
        bike_options = list(bike_map.keys())
        preselected_id = st.session_state.get("repair_bike_id")
        preselected_label = next((label for label, bid in bike_map.items() if bid == preselected_id), None)
        bike_label = st.selectbox(
            "Велосипед",
            options=bike_options,
            index=bike_options.index(preselected_label) if preselected_label in bike_options else None,
            placeholder="Выберите велосипед...",
        )

    employee_id = employee_map.get(employee_label)
    bike_id = bike_map.get(bike_label)
    comment = st.text_area("Комментарий")

    if st.button("➕ Добавить запчасть"):
        next_id = len(st.session_state["parts_rows"]) + 1
        st.session_state["parts_rows"].append({"row_id": next_id})
        st.rerun()

    for row in st.session_state["parts_rows"]:
        row_id = row["row_id"]
        rc1, rc2 = st.columns([3, 1])
        with rc1:
            st.selectbox(
                f"Запчасть #{row_id}",
                options=list(part_map.keys()),
                index=None,
                placeholder="Выберите запчасть...",
                key=f"part_label_{row_id}",
            )
        with rc2:
            st.number_input(f"Кол-во #{row_id}", min_value=1, value=1, step=1, key=f"part_qty_{row_id}")

    if st.button("Начать ремонт"):
        if bike_id is None:
            st.error("Выберите велосипед.")
        else:
            try:
                client.table("bikes").update({"status": "В ремонте"}).eq("id", bike_id).execute()
                st.success("Успешно: ремонт начат.")
            except Exception as error:
                st.error(f"Ошибка начала ремонта: {error}")

    if st.button("Завершить ремонт"):
        if bike_id is None or employee_id is None:
            st.error("Выберите мастера и велосипед.")
            return
        try:
            parts_payload = []
            for row in st.session_state["parts_rows"]:
                rid = row["row_id"]
                part_label = st.session_state.get(f"part_label_{rid}")
                part_id = part_map.get(part_label)
                qty = int(st.session_state.get(f"part_qty_{rid}", 1))
                if part_id is not None:
                    parts_payload.append({"part_id": part_id, "quantity": qty})

            work_type = detect_work_type("repair", len(parts_payload), comment)
            ticket = insert_repair_ticket(
                client,
                {
                    "bike_id": bike_id,
                    "employee_id": employee_id,
                    "comment": comment,
                    "work_type": work_type,
                },
            )
            if not ticket:
                st.error("Не удалось создать ремонтный тикет.")
                return

            ticket_id = ticket.get("id")
            if ticket_id and parts_payload:
                payload = [{"ticket_id": ticket_id, **row} for row in parts_payload]
                client.table("ticket_parts").insert(payload).execute()
                st.success("Успешно: запчасти добавлены.")

            client.table("bikes").update({"status": "Свободен"}).eq("id", bike_id).execute()
            ensure_work_day(client, employee_id)
            st.success("Успешно: ремонт завершен.")

            for row in st.session_state["parts_rows"]:
                rid = row["row_id"]
                st.session_state.pop(f"part_label_{rid}", None)
                st.session_state.pop(f"part_qty_{rid}", None)
            st.session_state["parts_rows"] = []
            st.rerun()
        except Exception as error:
            st.error(f"Ошибка завершения ремонта: {error}")


def render_field_repairs_tab(client: Client) -> None:
    st.subheader("Выездной ремонт")
    tickets = fetch_table(client, "repair_tickets")
    bikes = fetch_table(client, "bikes")
    darkstores = fetch_table(client, "darkstores")
    ds_number_by_id = darkstore_number_map(darkstores)

    external = [t for t in tickets if t.get("is_external") is True or str(t.get("status") or "").lower() == "pending"]

    b_sn_by_id = {b.get("id"): b.get("sn") for b in bikes if b.get("id") is not None}
    b_plate_by_id = {b.get("id"): b.get("plate") for b in bikes if b.get("id") is not None}

    f1, f2, f3 = st.columns([1.6, 1.0, 1.4])
    with f1:
        q = st.text_input("Поиск (SN / Гос. номер / описание)")
    with f2:
        statuses = sorted({str(t.get("status") or "-") for t in external})
        status_filter = st.multiselect("Статус", options=statuses)
    with f3:
        ds_values = sorted({ds_number_by_id.get(t.get("current_darkstore_id"), "-") for t in external})
        ds_filter = st.multiselect("Даркстор", options=ds_values)

    filtered = external
    if q.strip():
        s = q.strip().lower()
        filtered = [
            t
            for t in filtered
            if s in str(t.get("problem_desc") or t.get("comment") or "").lower()
            or s in str(t.get("plate") or "").lower()
            or s in str(b_sn_by_id.get(t.get("bike_id"), "")).lower()
            or s in str(b_plate_by_id.get(t.get("bike_id"), "")).lower()
        ]
    if status_filter:
        filtered = [t for t in filtered if str(t.get("status") or "-") in status_filter]
    if ds_filter:
        filtered = [t for t in filtered if ds_number_by_id.get(t.get("current_darkstore_id"), "-") in ds_filter]

    rows = [
        {
            "Дата": t.get("created_at") or "-",
            "Даркстор": ds_number_by_id.get(t.get("current_darkstore_id"), "-"),
            "Тип техники": t.get("tech_type") or "-",
            "SN": b_sn_by_id.get(t.get("bike_id")) or "-",
            "Гос. номер": t.get("plate") or b_plate_by_id.get(t.get("bike_id")) or "-",
            "Статус": t.get("status") or "-",
            "Описание": t.get("problem_desc") or t.get("comment") or "-",
            "Фото до": t.get("photo_before") or "-",
        }
        for t in filtered
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True, height=520)


def render_repairs_tab(client: Client) -> None:
    tab_shop, tab_field = st.tabs(["Цех", "Выездной ремонт"])
    with tab_shop:
        render_repair_tab(client)
    with tab_field:
        render_field_repairs_tab(client)


def render_rental_tab(client: Client) -> None:
    st.subheader("Аренда")
    bikes = fetch_table(client, "bikes")
    darkstores = fetch_table(client, "darkstores")
    ds_number_by_id = darkstore_number_map(darkstores)

    sub_a, sub_b, sub_c = st.tabs(["B2C аренда", "B2B дарксторы", "Замены"])

    with sub_a:
        st.markdown("### B2C: отметки аренды (внутри ERP)")
        bike_options = [
            (f"{b.get('sn') or '-'} | {b.get('plate') or '-'} (ID: {b.get('id')})", b.get("id"))
            for b in bikes
            if b.get("id") is not None
        ]
        labels = [x[0] for x in bike_options]
        id_by_label = {x[0]: x[1] for x in bike_options}

        col1, col2 = st.columns(2)
        with col1:
            rent_label = st.selectbox("Велосипед (выдан в аренду)", options=labels, index=None, placeholder="Выберите...")
        with col2:
            return_label = st.selectbox("Велосипед (вернулся из аренды)", options=labels, index=None, placeholder="Выберите...")

        c1, c2 = st.columns(2)
        if c1.button("Пометить: в аренде"):
            bike_id = id_by_label.get(rent_label)
            if bike_id is None:
                st.error("Выберите велосипед.")
            else:
                try:
                    client.table("bikes").update({"status": "В аренде"}).eq("id", bike_id).execute()
                    st.success("Успешно: пометили как 'В аренде'.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Ошибка: {error}")

        if c2.button("Пометить: аренда завершена"):
            bike_id = id_by_label.get(return_label)
            if bike_id is None:
                st.error("Выберите велосипед.")
            else:
                try:
                    client.table("bikes").update({"status": "Свободен", "tech_status": "Ожидает ремонта"}).eq("id", bike_id).execute()
                    st.success("Успешно: аренда завершена, тех. состояние = 'Ожидает ремонта'.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Ошибка: {error}")

    with sub_b:
        st.markdown("### B2B: поставка/эвакуация")
        ds_options = [
            (f"{d.get('number') or d.get('id')} — {d.get('address') or d.get('name') or '-'}", d.get("id"))
            for d in darkstores
            if d.get("id") is not None
        ]
        ds_labels = [x[0] for x in ds_options]
        ds_id_by_label = {x[0]: x[1] for x in ds_options}

        free_bikes = [b for b in bikes if normalize_status(b.get("status")) == "Свободен" and b.get("id") is not None]
        free_options = [(f"{b.get('sn') or '-'} | {b.get('plate') or '-'} (ID: {b.get('id')})", b.get("id")) for b in free_bikes]
        free_labels = [x[0] for x in free_options]
        free_id_by_label = {x[0]: x[1] for x in free_options}

        st.markdown("#### Поставка на даркстор")
        col_a, col_b = st.columns([2, 1])
        with col_a:
            selected_free = st.multiselect("Свободные велосипеды", options=free_labels)
        with col_b:
            ds_label = st.selectbox("Даркстор", options=ds_labels, index=None, placeholder="Выберите...")
        if st.button("Поставить на даркстор"):
            ds_id = ds_id_by_label.get(ds_label)
            bike_ids = [free_id_by_label[lbl] for lbl in selected_free if free_id_by_label.get(lbl) is not None]
            if ds_id is None or not bike_ids:
                st.error("Выберите даркстор и велосипеды.")
            else:
                try:
                    client.table("bikes").update({"current_darkstore_id": ds_id, "status": "На дарксторе"}).in_("id", bike_ids).execute()
                    st.success("Успешно: поставка выполнена.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Ошибка поставки: {error}")

        st.divider()
        st.markdown("#### Эвакуация (запрос на вывоз)")
        ds_bikes = [b for b in bikes if b.get("current_darkstore_id") is not None and b.get("id") is not None]
        ds_bike_options = [
            (
                f"{b.get('sn') or '-'} | {b.get('plate') or '-'} | ДС {ds_number_by_id.get(b.get('current_darkstore_id'), '-')}"
                f" (ID: {b.get('id')})",
                b.get("id"),
            )
            for b in ds_bikes
        ]
        ds_bike_labels = [x[0] for x in ds_bike_options]
        ds_bike_id_by_label = {x[0]: x[1] for x in ds_bike_options}

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            evac_mark_label = st.selectbox("Велосипед (пометить: нужна эвакуация)", options=ds_bike_labels, index=None, placeholder="Выберите...")
        with col_e2:
            evac_do_label = st.selectbox("Велосипед (сделать вывоз)", options=ds_bike_labels, index=None, placeholder="Выберите...")

        e1, e2 = st.columns(2)
        if e1.button("Пометить: нужна эвакуация"):
            bike_id = ds_bike_id_by_label.get(evac_mark_label)
            if bike_id is None:
                st.error("Выберите велосипед.")
            else:
                try:
                    client.table("bikes").update({"status": "Нужна эвакуация"}).eq("id", bike_id).execute()
                    st.success("Успешно: пометка поставлена.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Ошибка: {error}")

        if e2.button("Выполнить вывоз"):
            bike_id = ds_bike_id_by_label.get(evac_do_label)
            if bike_id is None:
                st.error("Выберите велосипед.")
            else:
                try:
                    client.table("bikes").update({"current_darkstore_id": None, "status": "Свободен", "tech_status": "Ожидает ремонта"}).eq("id", bike_id).execute()
                    st.success("Успешно: вывоз выполнен, тех. состояние = 'Ожидает ремонта'.")
                    st.rerun()
                except Exception as error:
                    st.error(f"Ошибка: {error}")

    with sub_c:
        st.markdown("### Замена велосипеда")
        st.write("Используйте, когда нужно заменить байк на другой (в т.ч. с перевесом госномера).")

        bike_options = [
            (f"{b.get('sn') or '-'} | {b.get('plate') or '-'} (ID: {b.get('id')})", b.get("id"))
            for b in bikes
            if b.get("id") is not None
        ]
        labels = [x[0] for x in bike_options]
        id_by_label = {x[0]: x[1] for x in bike_options}

        c1, c2 = st.columns(2)
        with c1:
            old_label = st.selectbox("Старый байк (возвращается)", options=labels, index=None, placeholder="Выберите...")
        with c2:
            new_label = st.selectbox("Новый байк (выдаем)", options=labels, index=None, placeholder="Выберите...")

        transfer_plate = st.checkbox("Перевесить госномер со старого на новый", value=True)

        if st.button("Выполнить замену"):
            old_id = id_by_label.get(old_label)
            new_id = id_by_label.get(new_label)
            if old_id is None or new_id is None or old_id == new_id:
                st.error("Выберите два разных велосипеда.")
            else:
                ok, message = swap_bikes(client, old_id, new_id, transfer_plate=transfer_plate)
                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def month_window(today: date) -> tuple[datetime, datetime]:
    month_start = datetime(today.year, today.month, 1, 0, 0, 0)
    if today.month == 12:
        month_end = datetime(today.year + 1, 1, 1, 0, 0, 0)
    else:
        month_end = datetime(today.year, today.month + 1, 1, 0, 0, 0)
    return month_start, month_end


def load_month_tickets(client: Client, start_dt: datetime, end_dt: datetime) -> list[dict]:
    queries = [
        "id,created_at,employee_id,comment,work_type",
        "id,created_at,mechanic_id,comment,work_type",
        "id,created_at,comment,work_type",
    ]
    for query in queries:
        try:
            response = (
                client.table("repair_tickets")
                .select(query)
                .gte("created_at", start_dt.isoformat())
                .lt("created_at", end_dt.isoformat())
                .execute()
            )
            return response.data or []
        except Exception:
            continue
    return []


def load_work_days(client: Client) -> list[dict]:
    return fetch_table(client, "work_days")


def render_analytics_tab(client: Client) -> None:
    st.subheader("Аналитика")

    today = APP_TODAY
    start_dt, end_dt = month_window(today)
    tickets = load_month_tickets(client, start_dt, end_dt)
    employees = fetch_table(client, "employees")
    work_days = load_work_days(client)

    fact = len(tickets)
    month_plan = 500
    forecast = round((fact / 24) * 31, 2)

    k1, k2, k3 = st.columns(3)
    k1.metric("План на март", month_plan)
    k2.metric("Факт (месяц)", fact)
    k3.metric("Прогноз", forecast)

    employee_name_by_id = {
        x.get("id"): (x.get("name") or x.get("full_name") or f"Сотрудник {x.get('id')}")
        for x in employees
        if x.get("id") is not None
    }

    employee_field = "employee_id"
    if tickets and "employee_id" not in tickets[0]:
        employee_field = "mechanic_id"

    fact_by_employee = {}
    for row in tickets:
        emp_id = row.get(employee_field)
        if emp_id is None:
            continue
        fact_by_employee[emp_id] = fact_by_employee.get(emp_id, 0) + 1

    shift_by_employee = {}
    for wd in work_days:
        emp_id = wd.get("employee_id")
        if emp_id is None:
            continue
        day_value = wd.get("date") or wd.get("work_date")
        if day_value is None:
            continue
        shift_by_employee.setdefault(emp_id, set()).add(str(day_value))

    personal_rows = []
    for emp_id, emp_name in employee_name_by_id.items():
        emp_fact = fact_by_employee.get(emp_id, 0)
        shifts = len(shift_by_employee.get(emp_id, set()))
        percent = round((emp_fact / 90) * 100, 2)
        productivity = round(emp_fact / shifts, 2) if shifts else 0
        personal_rows.append(
            {
                "Мастер": emp_name,
                "Факт (мес)": emp_fact,
                "% плана": percent,
                "Смены": shifts,
                "Продуктивность": productivity,
            }
        )
    st.markdown("### Личные планы")
    st.dataframe(personal_rows, use_container_width=True, hide_index=True)

    st.markdown("### Типы работ (work_type)")
    work_type_map = {"parts": "Запчасти", "details": "Детали", "assembly": "Сборка", "repair": "Готово"}
    wt_counts: dict[str, int] = {k: 0 for k in work_type_map.values()}
    for row in tickets:
        wt = row.get("work_type")
        wt_label = work_type_map.get(str(wt), "Готово") if wt is not None else "Готово"
        wt_counts[wt_label] = wt_counts.get(wt_label, 0) + 1
    st.dataframe(
        [{"Тип работ": k, "Кол-во": v} for k, v in wt_counts.items()],
        use_container_width=True,
        hide_index=True,
    )

    start_7 = date(today.year, today.month, 18)
    dates = [start_7 + timedelta(days=i) for i in range(7)]
    by_day = {(emp_id, d.isoformat()): 0 for emp_id in employee_name_by_id for d in dates}
    for row in tickets:
        emp_id = row.get(employee_field)
        created = row.get("created_at")
        if emp_id is None or not created:
            continue
        day_key = str(created)[:10]
        if (emp_id, day_key) in by_day:
            by_day[(emp_id, day_key)] += 1

    seven_rows = []
    for emp_id, emp_name in employee_name_by_id.items():
        item = {"Мастер": emp_name}
        for d in dates:
            label = d.strftime("%d.%m")
            item[label] = by_day[(emp_id, d.isoformat())]
        seven_rows.append(item)
    st.markdown("### Статистика за 7 дней")
    st.dataframe(seven_rows, use_container_width=True, hide_index=True)


def load_curator_context(client: Client) -> tuple[list[dict], list[dict], list[dict], dict[str, int], dict[int, str]]:
    bikes = fetch_table(client, "bikes")
    darkstores = fetch_table(client, "darkstores")
    tickets = fetch_table(client, "repair_tickets")

    darkstore_id_by_number = {}
    darkstore_address_by_id = {}
    for row in darkstores:
        ds_id = row.get("id")
        if ds_id is None:
            continue
        darkstore_id_by_number[str(ds_id)] = ds_id
        if row.get("number") is not None:
            darkstore_id_by_number[str(row.get("number"))] = ds_id
        darkstore_address_by_id[ds_id] = row.get("address") or row.get("name") or "-"
    return bikes, darkstores, tickets, darkstore_id_by_number, darkstore_address_by_id


def render_curator_new_request(client: Client) -> None:
    st.markdown("### Новая заявка")
    bikes, darkstores, _, darkstore_id_by_number, darkstore_address_by_id = load_curator_context(client)
    ds_number_by_id = darkstore_number_map(darkstores)
    with st.form("curator_form"):
        darkstore_number = st.text_input("Номер даркстора")
        darkstore_id = darkstore_id_by_number.get(darkstore_number.strip())
        st.text_input("Адрес", value=darkstore_address_by_id.get(darkstore_id, "Не найден"), disabled=True)

        tech_type = st.selectbox("Тип техники", ["велосипед", "аккумулятор", "зарядка"])
        bike_plate = st.text_input("Номер велосипеда (гос номер)")
        problem = st.text_area("Что сломалось (problem_desc)")
        photo_before = st.text_input("Фото до ремонта (photo_before)")
        submit = st.form_submit_button("Отправить в цех")

    if submit:
        if not darkstore_number.strip() or not problem.strip():
            st.error("Укажите даркстор и описание проблемы.")
            return

        bike = next((x for x in bikes if str(x.get("plate") or "").strip().lower() == bike_plate.strip().lower()), None)
        bike_id = bike.get("id") if bike else None
        bike_darkstore_id = bike.get("current_darkstore_id") if bike else None

        problem_desc = problem.strip()
        if darkstore_id is not None and bike is not None and bike_darkstore_id != darkstore_id:
            problem_desc = f"[НЕ ЧИСЛИТСЯ НА ДАРКСТОРЕ {darkstore_number.strip()}] {problem_desc}"

        try:
            insert_repair_ticket(
                client,
                {
                    "bike_id": bike_id,
                    "current_darkstore_id": darkstore_id,
                    "problem_desc": problem_desc,
                    "photo_before": photo_before.strip() or None,
                    "tech_type": tech_type,
                    "plate": bike_plate.strip() or None,
                    "is_external": True,
                    "status": "Pending",
                    "work_type": "repair",
                },
            )
            if bike_id is not None:
                client.table("bikes").update({"tech_status": "Нужен ремонт"}).eq("id", bike_id).execute()
            st.success("Успешно: заявка отправлена в цех.")
            st.rerun()
        except Exception as error:
            st.error(f"Ошибка отправки заявки: {error}")


def render_curator_park(client: Client) -> None:
    st.markdown("### Мой парк")
    bikes, darkstores, _, darkstore_id_by_number, _ = load_curator_context(client)
    ds_number_by_id = darkstore_number_map(darkstores)
    park_ds_number = st.text_input("Номер даркстора", key="curator_park_ds_number")
    park_ds_id = darkstore_id_by_number.get(park_ds_number.strip())
    if park_ds_id is not None:
        park_rows = [
            {
                "Серийный номер": x.get("sn"),
                "Гос. номер": x.get("plate"),
                "Даркстор": ds_number_by_id.get(x.get("current_darkstore_id"), "-"),
                "Статус": normalize_status(x.get("status")),
                "Тех. состояние": x.get("tech_status") or "Не указан",
            }
            for x in bikes
            if x.get("current_darkstore_id") == park_ds_id
        ]
        st.dataframe(park_rows, use_container_width=True, hide_index=True)
    elif park_ds_number.strip():
        st.info("Даркстор не найден.")


def render_curator_requests(client: Client) -> None:
    st.markdown("### Мои заявки")
    _, _, tickets, darkstore_id_by_number, _ = load_curator_context(client)
    req_ds_number = st.text_input("Номер даркстора", key="curator_req_ds_number")
    req_ds_id = darkstore_id_by_number.get(req_ds_number.strip())
    if req_ds_id is not None:
        req_rows = [
            {
                "Дата": t.get("created_at") or "-",
                "Статус": t.get("status") or "-",
                "Тип техники": t.get("tech_type") or "-",
                "Гос. номер": t.get("plate") or "-",
                "Описание": t.get("problem_desc") or t.get("comment") or "-",
            }
            for t in tickets
            if t.get("current_darkstore_id") == req_ds_id
        ]
        st.dataframe(req_rows, use_container_width=True, hide_index=True)
    elif req_ds_number.strip():
        st.info("Даркстор не найден.")


st.set_page_config(page_title="Vanta ERP", layout="wide")

# NEW: apply theme before rendering UI
apply_dark_premium_theme()
render_premium_header()

client = get_supabase_client()
if client:
    if "system_mode" not in st.session_state:
        st.session_state["system_mode"] = "internal"

    mode_cols = st.columns([8, 1, 1])
    if mode_cols[1].button("Внутренняя"):
        st.session_state["system_mode"] = "internal"
    if mode_cols[2].button("Куратор"):
        st.session_state["system_mode"] = "curator"

    if st.session_state["system_mode"] == "internal":
        tab_bikes, tab_rental, tab_repairs, tab_analytics = st.tabs(["Велосипеды", "Аренда", "Ремонты", "Аналитика"])
        with tab_bikes:
            render_bikes_tab(client)
        with tab_rental:
            render_rental_tab(client)
        with tab_repairs:
            render_repairs_tab(client)
        with tab_analytics:
            render_analytics_tab(client)
    else:
        st.subheader("Кабинет куратора")
        tab_new, tab_requests, tab_park = st.tabs(["Новая заявка", "Мои заявки", "Мой парк"])
        with tab_new:
            render_curator_new_request(client)
        with tab_requests:
            render_curator_requests(client)
        with tab_park:
            render_curator_park(client)