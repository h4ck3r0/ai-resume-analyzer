import { createBrowserRouter } from "react-router";
import { Root } from "./components/Root";
import { Home } from "./pages/Home";
import { Analyzer } from "./pages/Analyzer";
import { TemplateGenerator } from "./pages/TemplateGenerator";
import { About } from "./pages/About";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: Root,
    children: [
      { index: true, Component: Home },
      { path: "analyzer", Component: Analyzer },
      { path: "template", Component: TemplateGenerator },
      { path: "about", Component: About },
    ],
  },
]);
