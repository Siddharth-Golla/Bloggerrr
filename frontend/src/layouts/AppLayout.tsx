import { Outlet } from "react-router-dom";

import Header from "../components/Header";
import Sidebar from "../components/Sidebar";

function AppLayout() {
  return (
    <div className="app-layout">
      <Header />

      <div className="app-body">
        <Sidebar />

        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppLayout;