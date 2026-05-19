import streamlit as st
import time
import re



# =========================
# SESSION STATE INIT
# =========================

if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

if "aviso_aceptado" not in st.session_state:
    st.session_state.aviso_aceptado = False

if "_cambio" not in st.session_state:
    st.session_state._cambio = False

if "forzar_formulario" not in st.session_state:
    st.session_state.forzar_formulario = False

if "formulario_completado" not in st.session_state:
    st.session_state.formulario_completado = False

if "sistema" not in st.session_state:
    st.session_state.sistema = None

if "fluido" not in st.session_state:
    st.session_state.fluido = None

# =========================
# ESTILO
# =========================

st.markdown("""
<style>

h1 {
    color: black !important;
}

[data-testid="stAppViewContainer"] {
    background-color: white;
}

.block-container {
    padding-top: 4rem;
    padding-bottom: 1rem;
}

.titulo {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: black;
}

.nombre {
    text-align: center;
    font-size: 20px;
    color: black;
}


/* BOTÓN EMPEZAR */

div.stButton > button {
    display: block;
    margin: 40px auto;
    background-color: #c62828;
    color: white;
    font-size: 18px;
    padding: 10px 35px;
    border-radius: 10px;
    border: none;
}

/* ALERTA */

.alerta {
    background-color: #fff3cd;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ffeeba;
    color: #856404;
    font-weight: 600;
}

/* BOTÓN AUTORIZACIÓN */

div.stButton > button {
    font-size: 14px !important;
    padding: 8px 18px !important;
    min-width: 150px !important;
    white-space: nowrap !important;
    word-break: keep-all !important;
    text-align: center !important;
}

.autorizar-btn {
    margin-top: 2px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# INICIO
# =========================

if st.session_state.pantalla == "inicio":
    if st.session_state.get("_cambio", False):
        st.stop()

    st.markdown('<div class="titulo">💧 Sistema Hidráulico de Bombeo 💧</div>', unsafe_allow_html=True)
    st.markdown('<div class="nombre">Delsair Jose Montalvo Maza 👨🏽‍🔧 ®</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image("logo.png", width=230)

    if st.button("Empezar"):
        st.session_state.pantalla = "datos"
        st.session_state._cambio = True
        st.rerun()

# =========================
# SISTEMA
# =========================

if st.session_state.pantalla == "datos":
    if "timer_iniciado" not in st.session_state:
        time.sleep(3)
        st.session_state.timer_iniciado = True
        st.session_state.forzar_formulario = True

    st.markdown("<h1 style='text-align:center;'>SISTEMA</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("sistema.png", use_container_width=True)

    # =========================
    # FORMULARIO
    # =========================

    @st.dialog("⚠️ AUTORIZACIÓN DE DATOS")
    def formulario():

        st.write("""
El sistema realiza los cálculos con base en los datos proporcionados por el usuario; por tanto, la precisión de los resultados depende directamente de la calidad de dicha información.
        """)

        autorizacion = st.checkbox(
            "Certifico que los datos ingresados son correctos y asumo la responsabilidad sobre los resultados derivados de su uso."
        )

        nombre = st.text_input("Nombres y Apellidos")
        ciudad = st.text_input("Ciudad")
        edad = st.text_input("Edad")

        if edad:
            if edad.isdigit() and int(edad) < 18:
                st.warning("Debes ser mayor de edad para contemplar la autorización")
        if st.button("Aceptar"):

            error = False

            if not nombre or not ciudad or not edad:
                error = True

            if edad.isdigit():
                if int(edad) < 18:
                    error = True
            else:
                error = True

            if not autorizacion:
                error = True

            if not error:
                st.session_state.nombre = nombre
                st.session_state.ciudad = ciudad
                st.session_state.edad = edad

                st.session_state.aviso_aceptado = True
                st.session_state.formulario_completado = True
                st.session_state.forzar_formulario = False

                st.rerun()


    # =========================
    # CONTROL UI
    # =========================

    if st.session_state.pantalla == "datos" and not st.session_state.aviso_aceptado:

        if st.session_state.forzar_formulario and not st.session_state.formulario_completado:
            formulario()

        if not st.session_state.formulario_completado:
            st.session_state.forzar_formulario = True

            st.markdown("""
            <style>
            .fila-alerta {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 20px;
            }

            .alerta-box {
                background-color: #fff3cd;
                padding: 15px;
                border-radius: 10px;
                border: 1px solid #ffeeba;
                color: #856404;
                font-weight: 600;
                flex: 1;
            }

            </style>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([4, 1], vertical_alignment="center")
            with col1:
                st.markdown("""
                <div class="alerta-box">
                ⚠️ Debes completar la autorización para continuar con el sistema.
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("<div style='display:flex; align-items:center; height:100%;'>", unsafe_allow_html=True)
                if st.button("AUTORIZACIÓN"):
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            st.stop()

# =========================
# MOSTRAR SOLO SI YA AUTORIZÓ
# =========================

if st.session_state.pantalla == "datos" and st.session_state.aviso_aceptado:

    # =========================
    # ESTILO
    # =========================

    st.markdown("""
    <style>
    label, .stMarkdown, p, h1, h2, h3 {
        color: black !important;
    }

    input {
        background-color: #e3f2fd !important;
        color: black !important;
    }

    button[kind="secondary"] {
        padding: 2px 6px !important;
        font-size: 11px !important;
        min-height: 28px !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.success(f"Bienvenido {st.session_state.nombre}")

    # =========================
    # SISTEMA DE UNIDADES
    # =========================

    st.markdown("<h3>¿Qué sistema manejas?</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🌎 INTERNACIONAL (SI)"):
            st.session_state.sistema = "SI"

    with col2:
        if st.button("🇺🇸 INGLÉS (US)"):
            st.session_state.sistema = "EN"

    if st.session_state.sistema is None:
        st.warning("⚠️ Selecciona un sistema de unidades")
        st.stop()

    # =========================
    # UNIDADES + FLUIDOS
    # =========================

    if st.session_state.sistema == "SI":
        u_Q, u_L, u_D, u_e, u_z = "[m³/s]", "[m]", "[m]", "[mm]", "[m]"
        u_rho = "kg/m³"
        u_mu = "Pa·s"

        fluidos = {
            "Agua (20°C)": {"rho": 998, "mu": 0.001},
            "Aceite": {"rho": 850, "mu": 0.05},
            "Glicerina": {"rho": 1260, "mu": 1.49}
        }

    else:
        u_Q, u_L, u_D, u_e, u_z = "[ft³/s]", "[ft]", "[ft]", "[in]", "[ft]"
        u_rho = "slug/ft³"
        u_mu = "lb·s/ft²"

        fluidos = {
            "Water (68°F)": {"rho": 1.94, "mu": 2.1e-5},
            "Light oil": {"rho": 1.65, "mu": 0.001},
            "Glycerin": {"rho": 2.45, "mu": 0.031}
        }

    # =========================
    # FLUIDO
    # =========================

    st.markdown("<h3>💧 Fluido de trabajo</h3>", unsafe_allow_html=True)

    if "fluido_confirmado" not in st.session_state:
        st.session_state.fluido_confirmado = False

    fluido_sel = st.selectbox("Selecciona el fluido", list(fluidos.keys()))

    rho = fluidos[fluido_sel]["rho"]
    mu = fluidos[fluido_sel]["mu"]

    st.markdown(f"""
    • **Densidad (ρ):** {rho} {u_rho}  
    • **Viscosidad (μ):** {mu} {u_mu}
    """)

    if not st.session_state.fluido_confirmado:
        if st.button("✅ Confirmar fluido"):
            st.session_state.fluido_confirmado = True
            st.session_state["rho"] = rho
            st.session_state["mu"] = mu
            st.session_state["fluido"] = fluido_sel
            st.rerun()

    if not st.session_state.fluido_confirmado:
        st.warning("⚠️ Debes confirmar el fluido")
        st.stop()

    st.markdown("---")

    # =========================
    # FUNCIÓN CAMPO
    # =========================

    def campo(nombre, key):
        col1, col2 = st.columns([3,2])
        with col1:

            st.markdown(nombre)
        with col2:
            valor = st.text_input("", key=key)

        return valor

    # =========================
    # CATÁLOGO ACCESORIOS
    # =========================

    catalogo = {
        "Codo 90°": 0.9,
        "Codo 45°": 0.4,
        "Válvula compuerta": 0.2,
        "Válvula globo": 10,
        "Válvula check": 2,
        "Entrada brusca": 0.5,
        "Salida libre": 1,
        "Tee recto": 0.6,
        "Tee lateral": 1.8,
        "Reducción": 0.3,
        "Expansión": 1
    }

    if "acc_succion" not in st.session_state:
        st.session_state.acc_succion = []

    if "acc_descarga" not in st.session_state:
        st.session_state.acc_descarga = []

    # =========================
    # SUCCIÓN
    # =========================

    st.markdown("<h3>🔼 SUCCIÓN</h3>", unsafe_allow_html=True)

    Q = campo(f"Caudal (Q) {u_Q}", "Q")
    L_s = campo(f"Longitud (Lₛ) {u_L}", "L_s")
    D_s = campo(f"Diámetro (Dₛ) {u_D}", "D_s")
    e_s = campo(f"Rugosidad (εₛ) {u_e}", "e_s")
    z_1 = campo(f"Altura (Z₁) {u_z}", "z_1")

    st.markdown("**Accesorios en succión:**")

    c1, c2 = st.columns([2,3])

    with c1:
        sel_s = st.selectbox("Accesorio", list(catalogo.keys()), key="sel_s")
        cant_s = st.number_input("Cantidad", min_value=1, step=1, key="cant_s")

        if st.button("➕ Agregar", key="add_s"):
            st.session_state.acc_succion.append({
                "nombre": sel_s,
                "K": catalogo[sel_s],
                "cantidad": cant_s
            })

            st.rerun()

    with c2:

        total_K_s = 0

        for i, acc in enumerate(st.session_state.acc_succion):
            Kt = acc["K"] * acc["cantidad"]
            total_K_s += Kt

            a, b = st.columns([6,1])

            with a:
                st.markdown(f"• {acc['nombre']} ({acc['cantidad']}) → K={round(Kt,2)}")

            with b:
                if st.button("✖", key=f"del_s_{i}", type="secondary"):
                    st.session_state.acc_succion.pop(i)
                    st.rerun()

        st.markdown(f"**K total succión: {round(total_K_s,2)}**")

    st.markdown("---")

    # =========================
    # DESCARGA
    # =========================

    st.markdown("<h3>🔽 DESCARGA</h3>", unsafe_allow_html=True)

    L_d = campo(f"Longitud (Lᵈ) {u_L}", "L_d")
    D_d = campo(f"Diámetro (Dᵈ) {u_D}", "D_d")
    e_d = campo(f"Rugosidad (εᵈ) {u_e}", "e_d")
    z_2 = campo(f"Altura (Z₂) {u_z}", "z_2")

    st.markdown("**Accesorios en descarga:**")

    c1, c2 = st.columns([2,3])

    with c1:
        sel_d = st.selectbox("Accesorio", list(catalogo.keys()), key="sel_d")
        cant_d = st.number_input("Cantidad", min_value=1, step=1, key="cant_d")

        if st.button("➕ Agregar", key="add_d"):
            st.session_state.acc_descarga.append({
                "nombre": sel_d,
                "K": catalogo[sel_d],
                "cantidad": cant_d
            })

            st.rerun()

    with c2:
        total_K_d = 0

        for i, acc in enumerate(st.session_state.acc_descarga):
            Kt = acc["K"] * acc["cantidad"]
            total_K_d += Kt

            a, b = st.columns([6,1])

            with a:
                st.markdown(f"• {acc['nombre']} ({acc['cantidad']}) → K={round(Kt,2)}")

            with b:
                if st.button("✖", key=f"del_d_{i}", type="secondary"):
                    st.session_state.acc_descarga.pop(i)
                    st.rerun()

        st.markdown(f"**K total descarga: {round(total_K_d,2)}**")

    # =========================
    # BOTÓN CARGAR DATOS
    # =========================

    if st.button("🟢 CARGAR DATOS"):

        campos = [Q, L_s, D_s, e_s, z_1, L_d, D_d, e_d, z_2]

        if any(c is None or c == "" for c in campos):
            st.error("⚠️ Faltan datos")
            st.stop()

        st.session_state.datos = {
            "Q": float(Q),
            "L_s": float(L_s),
            "D_s": float(D_s),
            "e_s": float(e_s),
            "z_1": float(z_1),
            "L_d": float(L_d),
            "D_d": float(D_d),
            "e_d": float(e_d),
            "z_2": float(z_2),
            "K_s": total_K_s,
            "K_d": total_K_d,
            "rho": st.session_state["rho"],
            "mu": st.session_state["mu"],
            "fluido": st.session_state["fluido"]
        }

        st.session_state.pantalla = "resultados"

        st.rerun()

# =========================
# PANTALLA RESULTADOS
# =========================

if st.session_state.pantalla == "resultados":
    import os

    # =========================
    # ESTILO
    # =========================

    st.markdown("""
    <style>

    [data-testid="stAppViewContainer"] {
        background-color: white;
    }

    p, h1, h2, h3, li, span, div {
        color: black !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>📋 RESUMEN</h1>", unsafe_allow_html=True)
    datos = st.session_state.get("datos")

    if not datos:
        st.error("No hay datos cargados")
        st.stop()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    img_succion = os.path.join(BASE_DIR, "succion.png")
    img_descarga = os.path.join(BASE_DIR, "descarga.png")
    img_accesorios = os.path.join(BASE_DIR, "accesorios.png")

    # =========================
    # UNIDADES
    # =========================

    if st.session_state.sistema == "SI":
        u_Q, u_L, u_D, u_e, u_z = "m³/s", "m", "m", "mm", "m"

    else:
        u_Q, u_L, u_D, u_e, u_z = "ft³/s", "ft", "ft", "in", "ft"

    st.markdown("---")

    # =========================
    # SUCCIÓN
    # =========================

    col1, col2 = st.columns([1,3])

    with col1:

        if os.path.exists(img_succion):
            st.image(img_succion, use_container_width=True)

    with col2:

        st.markdown("### 🔼 SUCCIÓN")

        st.markdown(f"""
        • **Caudal (Q):** {datos['Q']} {u_Q}  
        • **Longitud (Lₛ):** {datos['L_s']} {u_L}  
        • **Diámetro (Dₛ):** {datos['D_s']} {u_D}  
        • **Rugosidad (εₛ):** {datos['e_s']} {u_e}  
        • **Altura (Z₁):** {datos['z_1']} {u_z}  
        • **K total:** {datos['K_s']}  
        """)

    st.markdown("---")

    # =========================
    # DESCARGA
    # =========================

    col1, col2 = st.columns([1,3])

    with col1:

        if os.path.exists(img_descarga):
            st.image(img_descarga, use_container_width=True)

    with col2:
        st.markdown("### 🔽 DESCARGA")

        st.markdown(f"""
        • **Longitud (Lᵈ):** {datos['L_d']} {u_L}  
        • **Diámetro (Dᵈ):** {datos['D_d']} {u_D}  
        • **Rugosidad (εᵈ):** {datos['e_d']} {u_e}  
        • **Altura (Z₂):** {datos['z_2']} {u_z}  
        • **K total:** {datos['K_d']}  
        """)

    st.markdown("---")

    # =========================
    # ACCESORIOS
    # =========================

    col1, col2 = st.columns([1,3])

    with col1:
        if os.path.exists(img_accesorios):
            st.image(img_accesorios, use_container_width=True)

    with col2:
        st.markdown("### 🧩 ACCESORIOS")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("**Succión:**")

            if st.session_state.get("acc_succion"):
                for acc in st.session_state.acc_succion:
                    unidad = "unidad" if acc["cantidad"] == 1 else "unidades"
                    st.markdown(f"• {acc['nombre']} ({acc['cantidad']} {unidad})")

            else:
                st.markdown("• Ninguno")

        with colB:
            st.markdown("**Descarga:**")

            if st.session_state.get("acc_descarga"):
                for acc in st.session_state.acc_descarga:
                    unidad = "unidad" if acc["cantidad"] == 1 else "unidades"
                    st.markdown(f"• {acc['nombre']} ({acc['cantidad']} {unidad})")

            else:
                st.markdown("• Ninguno")

    st.markdown("---")

    # =========================
    # BOTONES
    # =========================

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 TODO CORRECTO"):
            st.session_state.pantalla = "proceso"
            st.rerun()

    with col2:
        if st.button("👎 ME EQUIVOQUÉ"):
            st.session_state.pantalla = "datos"
            st.rerun()

# ==========================
# PANTALLA PROCESO Y CURVAS
# ==========================

if st.session_state.get("pantalla") == "proceso":

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    st.markdown("""

    <style>

    p, h1, h2, h3, div, span { color: black !important; }

    input { background-color: #e3f2fd !important; color: black !important; }

    .katex { color: black !important; }

    table {
        border-collapse: collapse;
        margin: auto;
        font-size: 12px;
    }

    th, td {
        border: 1px solid black !important;
        padding: 4px 6px !important;
        text-align: center !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>🧠 DESARROLLO DE CÁLCULOS Y CURVAS</h1>", unsafe_allow_html=True)

    datos = st.session_state.get("datos")

    if not datos:
        st.error("No hay datos")
        st.stop()

    # =========================
    # UNIDADES
    # =========================

    if st.session_state.get("sistema") == "SI":
        g = 9.81
        u_L, u_Q, u_v = "m", "m³/s", "m/s"
        u_rho, u_mu, u_H = "kg/m³", "Pa·s", "m"

    else:
        g = 32.2
        u_L, u_Q, u_v = "ft", "ft³/s", "ft/s"
        u_rho, u_mu, u_H = "slug/ft³", "lb·s/ft²", "ft"

    rho, mu = datos["rho"], datos["mu"]

    # =========================

    # FUNCIONES DE CÁLCULO

    # =========================

    def colebrook_NR(Re, e, D):
        def F(f): return 1/np.sqrt(f) + 2*np.log10((e/(3.7*D)) + (2.51/(Re*np.sqrt(f))))
        def dF(f):
            term = (e/(3.7*D)) + (2.51/(Re*np.sqrt(f)))
            return (-1/(2*f**(3/2))) + (2 * (-(2.51/(2*Re*f**(3/2)))) / (term * np.log(10)))

        f, tol, data = 0.02, 1e-6, []
        for i in range(30):
            f_old = f
            f = f - F(f)/dF(f)
            error = abs(f - f_old)
            data.append([i+1, f, error])
            if error < tol: break

        return f, pd.DataFrame(data, columns=["Iteración", "f", "|Error|"]), tol

    def colebrook_simple(Re, e, D):
        f = 0.02
        for _ in range(25):
            f = 1 / (-2 * np.log10(e/(3.7*D) + 2.51/(Re*np.sqrt(f))))**2

        return f

    def imprimir_bloque(nombre, sub, Q, D, L, e, K):
        st.markdown(f"<h2>🔹 {nombre}</h2>", unsafe_allow_html=True)

        
        # ÁREA

        A = np.pi * D**2 / 4

        st.markdown("### Área")

        st.latex(f"A_{{{sub}}} = \\frac{{\\pi D^2}}{{4}}")

        st.latex(f"A_{{{sub}}} = \\frac{{\\pi ({D}\\,{u_L})^2}}{{4}}")

        st.write(f"**Resultado:** {A:.6f} {u_L}²")

        
        # VELOCIDAD

        V = Q / A

        st.markdown("### Velocidad")

        st.latex(f"V_{{{sub}}} = \\frac{{Q}}{{A}}")

        st.latex(f"V_{{{sub}}} = \\frac{{{Q}\\,{u_Q}}}{{{A:.6f}\\,{u_L}^2}}")

        st.write(f"**Resultado:** {V:.6f} {u_v}")


        # REYNOLDS

        Re = rho * V * D / mu

        st.markdown("### Reynolds")

        st.latex(f"Re_{{{sub}}} = \\frac{{\\rho V D}}{{\\mu}}")

        st.latex(f"Re_{{{sub}}} = \\frac{{({rho}\\,{u_rho})({V:.4f}\\,{u_v})({D}\\,{u_L})}}{{{mu}\\,{u_mu}}}")

        st.write(f"**Resultado:** {Re:.2f}")


        # FRICCIÓN

        st.markdown("### Factor de fricción")

        if Re < 2000:

            f = 64 / Re

            st.latex(f"f = \\frac{{64}}{{Re}} = \\frac{{64}}{{{Re:.2f}}}")

        else:

            f, df, tol = colebrook_NR(Re, e, D)

            st.latex(r"\frac{1}{\sqrt{f}} = -2 \log_{10} \left( \frac{\epsilon/D}{3.7} + \frac{2.51}{Re\sqrt{f}} \right)")

            st.write(f"Método: Newton-Raphson | Tolerancia: {tol}")

            st.markdown(df.to_html(index=False), unsafe_allow_html=True)

        st.write(f"**Resultado (f):** {f:.6f}")


        # PÉRDIDAS

        hf = f * (L/D) * (V**2 / (2*g))

        hL = K * (V**2 / (2*g))

        st.markdown("### Pérdidas")

        st.latex(f"h_{{f,{sub}}} = f \\frac{{L}}{{D}} \\frac{{V^2}}{{2g}}")

        st.latex(f"h_{{f,{sub}}} = {f:.5f} \\frac{{{L}\\,{u_L}}}{{{D}\\,{u_L}}} \\frac{{({V:.4f}\\,{u_v})^2}}{{2({g})}}")

        st.write(f"**Fricción:** {hf:.6f} {u_L}")
        

        st.latex(f"h_{{L,{sub}}} = K \\frac{{V^2}}{{2g}}")

        st.latex(f"h_{{L,{sub}}} = {K} \\frac{{({V:.4f}\\,{u_v})^2}}{{2({g})}}")

        st.write(f"**Accesorios:** {hL:.6f} {u_L}")

        st.markdown("---")


    # Ejecución de bloques de cálculo

    imprimir_bloque("SUCCIÓN","s",datos["Q"],datos["D_s"],datos["L_s"],datos["e_s"],datos["K_s"])

    imprimir_bloque("DESCARGA","d",datos["Q"],datos["D_d"],datos["L_d"],datos["e_d"],datos["K_d"])

    # =========================================================
    # SECCIÓN DE CURVAS
    # =========================================================
    st.markdown("<h1 style='text-align:center;'>📈 CURVA DEL SISTEMA</h1>", unsafe_allow_html=True)
    
    D_prom = (datos["D_s"] + datos["D_d"]) / 2
    L_tot = (datos["L_s"] + datos["L_d"])
    K_tot = (datos["K_s"] + datos["K_d"])
    e_prom = (datos["e_s"] + datos["e_d"]) / 2
    dz = abs(datos["z_2"] - datos["z_1"])

    Q_max = max(datos["Q"] * 3, 1)
    Q_vals = np.linspace(0.001, Q_max, 300)
    Hs_vals = []

    for Q_i in Q_vals:
        A_i = np.pi * D_prom**2 / 4
        V_i = Q_i / A_i
        Re_i = rho * V_i * D_prom / mu
        f_i = 64/Re_i if Re_i < 2000 else colebrook_simple(Re_i, e_prom, D_prom)
        Hs = dz + (f_i * (L_tot/D_prom) + K_tot) * (V_i**2/(2*g))
        Hs_vals.append(Hs)

    coef = np.polyfit(Q_vals, Hs_vals, 2)
    st.markdown("## 🔷 Curva del Sistema")
    st.latex(r"H_s(Q) = \Delta z + \left( f \frac{L}{D} + \sum K \right) \frac{V^2}{2g}")
    st.latex(f"H_s(Q) = {coef[2]:.4f} + {coef[0]:.4f}Q^2")

    fig1, ax1 = plt.subplots()
    ax1.plot(Q_vals, Hs_vals, color="blue", label="Sistema")
    ax1.set_xlabel(f"Q ({u_Q})"); ax1.set_ylabel(f"H ({u_H})")
    ax1.grid(); ax1.legend()
    st.pyplot(fig1)

    # ===================================
    # INTEGRACIÓN DE PANTALLA CONCLUSIÓN 
    # ===================================
    st.markdown("---")
    st.markdown("<h1 style='text-align:center;'>✅ CONCLUSIÓN</h1>", unsafe_allow_html=True)

    # Cálculo de la Cabeza Requerida evaluando el Q de entrada en la ecuación hallada
    Q_diseno = datos["Q"]
    H_requerida = coef[2] + coef[0] * (Q_diseno**2)

    # Unidades para el resumen
    if st.session_state.get("sistema") == "SI":
        u_Q_fin, u_L_fin, u_H_fin = "m³/s", "m", "m"
    else:
        u_Q_fin, u_L_fin, u_H_fin = "ft³/s", "ft", "ft"

    st.markdown("## 📋 Resumen Final")
    st.markdown(f"""
    - **Caudal de diseño (Q):** {Q_diseno} {u_Q_fin}
    - **Altura requerida del sistema (H):** {H_requerida:.4f} {u_H_fin}
    - **Longitud de succión (Ls):** {datos['L_s']} {u_L_fin}
    - **Longitud de descarga (Ld):** {datos['L_d']} {u_L_fin}
    - **Diámetro de succión (Ds):** {datos['D_s']} {u_L_fin}
    - **Diámetro de descarga (Dd):** {datos['D_d']} {u_L_fin}
    """)

    # ========================
    # INTEGRACIÓN DE CRÉDITOS
    # ========================
    st.markdown("---")
    st.markdown("<h1 style='text-align:center;'>🎓 CRÉDITOS</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; color: black;'>
    <h2>Sistema Hidráulico de Bombeo</h2>
    <h3>👨🏽‍🔧 Desarrollado por:</h3>
    <p><strong>Delsair Jose Montalvo Maza</strong></p>
    <p>Ingeniería Mecánica</p>
    <p>© 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("✅ Cálculos y reporte finalizados correctamente")
