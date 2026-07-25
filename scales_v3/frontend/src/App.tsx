import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { DashboardPage } from "./pages/DashboardPage";
import { ReviewPage } from "./pages/ReviewPage";
import { ResultsPage } from "./pages/ResultsPage";
import { ExplainPage } from "./pages/ExplainPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/exams/:examId/review" element={<ReviewPage />} />
        <Route path="/exams/:examId/results" element={<ResultsPage />} />
        <Route path="/exams/:examId/explain" element={<ExplainPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
