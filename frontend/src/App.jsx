import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Header from "./components/header";
import Body from "./components/body";
import Sidebar from "./components/sidebar";

let router = createBrowserRouter([
  {
    path: "/",
    loader: () => ({ message: "Hello, world!" }),
    Component() {
      return (
        <div className="drawer">
          <input id="my-drawer" type="checkbox" className="drawer-toggle" />
          <div className="bg-base-100 min-h-screen drawer-content">
            <Header />
            <Body />
          </div>

          <div className="drawer-side">
            <label htmlFor="my-drawer" className="drawer-overlay"></label>
            <Sidebar />
          </div>
        </div>
      );
    },
  },
]);

export default function App() {
  return <RouterProvider router={router} fallbackElement={<p>Loading...</p>} />;
}

if (import.meta.hot) {
  import.meta.hot.dispose(() => router.dispose());
}
