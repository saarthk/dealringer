import { createBrowserRouter, RouterProvider } from "react-router-dom";
import RootLayout from "./layouts/root-layout";
import HomePage from "./routes/home-page";
import SearchPage from "./routes/search-page";
import { loader as phonesLoader } from "./routes/home-page";
import { loader as searchedPhonesLoader } from "./routes/search-page";

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      {
        path: "/",
        element: <HomePage />,
        loader: phonesLoader,
      },
      {
        path: "/search",
        element: <SearchPage />,
        loader: searchedPhonesLoader,
      },
    ],
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}

if (import.meta.hot) {
  import.meta.hot.dispose(() => router.dispose());
}
