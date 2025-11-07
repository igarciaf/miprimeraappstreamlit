import React, { useState } from "react";

function App() {
  const [pantalla, setPantalla] = useState("principal");
  const [comunaSeleccionada, setComunaSeleccionada] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [mensajes, setMensajes] = useState([]);

  const comunasSantiago = [
    "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central",
    "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja",
    "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo",
    "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén",
    "Providencia", "Pudahuel", "Puente Alto", "Quilicura", "Quinta Normal",
    "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón",
    "Santiago Centro", "Vitacura"
  ];

  // Enviar mensaje con Enter
  const handleEnviarMensaje = (e) => {
    e.preventDefault();
    if (mensaje.trim() !== "") {
      setMensajes([...mensajes, { texto: mensaje, emisor: "usuario" }]);
      setMensaje("");
    }
  };

  // Contenido dinámico según la pantalla
  const renderPantalla = () => {
    switch (pantalla) {
      case "principal":
        return (
          <div className="p-4 space-y-4 mt-16 mb-20">
            <h2 className="text-xl font-semibold mb-2 text-center">
              Encuentra el servicio que necesitas
            </h2>

            <div className="space-y-2">
              <button
                onClick={() => setPantalla("servicios")}
                className="w-full p-4 bg-gray-100 rounded-xl hover:bg-gray-200 transition"
              >
                Buscar servicios disponibles
              </button>
            </div>
          </div>
        );

      case "servicios":
        return (
          <div className="p-4 space-y-4 mt-16 mb-20">
            <h2 className="text-xl font-semibold mb-2 text-center">
              Selecciona tu comuna
            </h2>
            <select
              value={comunaSeleccionada}
              onChange={(e) => setComunaSeleccionada(e.target.value)}
              className="w-full p-3 border rounded-xl"
            >
              <option value="">-- Selecciona una comuna --</option>
              {comunasSantiago.map((comuna) => (
                <option key={comuna} value={comuna}>
                  {comuna}
                </option>
              ))}
            </select>

            {comunaSeleccionada && (
              <div className="p-4 bg-gray-100 rounded-xl">
                Mostrando resultados en {comunaSeleccionada}.
              </div>
            )}
          </div>
        );

      case "chat":
        return (
          <div className="p-4 mt-16 mb-20">
            <h2 className="text-xl font-semibold text-center mb-4">Chat</h2>
            <div className="h-80 overflow-y-auto bg-gray-50 p-3 rounded-xl">
              {mensajes.map((m, i) => (
                <div
                  key={i}
                  className={`mb-2 p-2 rounded-xl w-fit ${
                    m.emisor === "usuario"
                      ? "bg-blue-200 ml-auto"
                      : "bg-gray-200"
                  }`}
                >
                  {m.texto}
                </div>
              ))}
            </div>

            <form
              onSubmit={handleEnviarMensaje}
              className="mt-4 flex items-center space-x-2"
            >
              <input
                type="text"
                value={mensaje}
                onChange={(e) => setMensaje(e.target.value)}
                placeholder="Escribe un mensaje..."
                className="flex-1 p-2 border rounded-xl"
              />
              <button
                type="submit"
                className="p-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition"
              >
                Enviar
              </button>
            </form>
          </div>
        );

      case "notificaciones":
        return (
          <div className="p-4 mt-16 mb-20">
            <h2 className="text-xl font-semibold text-center mb-4">
              Notificaciones
            </h2>
            <div className="bg-gray-50 p-4 rounded-xl text-center text-gray-500">
              No tienes notificaciones nuevas.
            </div>
          </div>
        );

      case "perfil":
        return (
          <div className="p-4 mt-16 mb-20">
            <h2 className="text-xl font-semibold text-center mb-4">
              Mi Perfil
            </h2>
            <div className="bg-gray-50 p-4 rounded-xl">
              <p>Nombre: Usuario de Ejemplo</p>
              <p>Servicios ofrecidos: Ninguno aún</p>
              <p>Valoraciones: ★★★★☆ (4.0)</p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="relative min-h-screen bg-white">
      {/* 🔝 Botón fijo con el nombre de la app */}
      <div className="fixed top-0 left-0 w-full bg-white shadow-md z-20 flex items-center justify-center py-3">
        <button
          onClick={() => setPantalla("principal")}
          className="text-2xl font-bold text-blue-600 hover:text-blue-800 transition"
        >
          Conecta
        </button>
      </div>

      {/* Contenido principal */}
      <div>{renderPantalla()}</div>

      {/* Barra inferior fija */}
      <div className="fixed bottom-0 left-0 w-full bg-white border-t shadow-md z-20 flex justify-around py-2">
        <button
          onClick={() => setPantalla("chat")}
          className="text-gray-600 hover:text-blue-600"
        >
          💬
        </button>
        <button
          onClick={() => setPantalla("notificaciones")}
          className="text-gray-600 hover:text-blue-600"
        >
          🔔
        </button>
        <button
          onClick={() => setPantalla("perfil")}
          className="text-gray-600 hover:text-blue-600"
        >
          👤
        </button>
      </div>
    </div>
  );
}

export default App;
