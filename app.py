import { useState } from "react";
import { Bell, MessageCircle, User } from "lucide-react";

export default function App() {
  const [page, setPage] = useState("home");

  return (
    <div className="relative min-h-screen flex flex-col bg-gray-50">
      {/* Contenido principal */}
      <div className="flex-1 overflow-y-auto pb-20">
        {page === "home" && <Home />}
        {page === "chat" && <Chat />}
        {page === "notifications" && <Notifications />}
        {page === "profile" && <Profile />}
      </div>

      {/* Barra inferior fija */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg flex justify-around items-center h-16">
        <button onClick={() => setPage("chat")} className="flex flex-col items-center text-gray-500 hover:text-blue-500">
          <MessageCircle size={24} />
          <span className="text-xs">Chats</span>
        </button>

        <button onClick={() => setPage("notifications")} className="flex flex-col items-center text-gray-500 hover:text-blue-500">
          <Bell size={24} />
          <span className="text-xs">Notificaciones</span>
        </button>

        <button onClick={() => setPage("profile")} className="flex flex-col items-center text-gray-500 hover:text-blue-500">
          <User size={24} />
          <span className="text-xs">Perfil</span>
        </button>
      </div>
    </div>
  );
}

function Home() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-center mb-4">Pantalla Principal</h1>
      <p className="text-gray-600 text-center">
        Aquí va el contenido principal, como los filtros y opciones de búsqueda.
      </p>
    </div>
  );
}

function Chat() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-center mb-4">Chats</h1>
      <p className="text-gray-600 text-center">Aquí aparecerán tus conversaciones.</p>
    </div>
  );
}

function Notifications() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-center mb-4">Notificaciones</h1>
      <p className="text-gray-600 text-center">
        Aquí verás cuando alguien vea tu perfil o te deje una valoración.
      </p>
    </div>
  );
}

function Profile() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-center mb-4">Tu Perfil</h1>
      <p className="text-gray-600 text-center">
        Aquí podrás ver y editar la información de tu perfil.
      </p>
    </div>
  );
}
