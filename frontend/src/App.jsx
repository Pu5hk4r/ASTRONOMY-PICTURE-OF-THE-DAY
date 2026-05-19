import { Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout";
import TodayPage from "./pages/TodayPage";
import SearchPage from "./pages/SearchPage";
import DatePage from "./pages/DatePage";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<TodayPage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/date" element={<DatePage />} />
        <Route path="/date/:dateParam" element={<DatePage />} />
      </Route>
    </Routes>
  );
}
