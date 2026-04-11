import { useState } from "react";
import {
  FileUp,
  CheckCircle2,
  AlertTriangle,
  Download,
  Sparkles,
  TrendingUp,
  Award,
} from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import { Button } from "../components/Button";
import { Card } from "../components/Card";
import { Badge } from "../components/Badge";
import { ScoreGauge } from "../components/ScoreGauge";

export function Analyzer() {
  const [jobDescription, setJobDescription] = useState("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);

  const analysisSteps = [
    "Resume extracted",
    "Matched requirements",
    "Skills analyzed",
    "Grammar checked",
    "Improvements ready",
  ];

  const handleAnalyze = () => {
    setAnalyzing(true);
    setShowResults(false);
    setAnalysisStep(0);

    const interval = setInterval(() => {
      setAnalysisStep((prev) => {
        if (prev >= analysisSteps.length - 1) {
          clearInterval(interval);
          setTimeout(() => {
            setAnalyzing(false);
            setShowResults(true);
          }, 500);
          return prev;
        }
        return prev + 1;
      });
    }, 1000);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedFile(e.target.files[0]);
    }
  };

  const mockResults = {
    score: 78,
    extractedSkills: [
      "JavaScript",
      "React",
      "TypeScript",
      "Node.js",
      "AWS",
      "Git",
      "REST APIs",
      "MongoDB",
      "CSS",
      "HTML",
    ],
    matchedRequirements: [
      "5+ years of software development experience",
      "Strong proficiency in JavaScript and React",
      "Experience with cloud platforms (AWS/Azure)",
      "Knowledge of RESTful API design",
      "Version control with Git",
    ],
    missingSkills: [
      "Docker/Kubernetes containerization",
      "CI/CD pipeline experience",
      "GraphQL API development",
      "Test-driven development (TDD)",
    ],
    percentile: 82,
    industryAverage: 65,
    grammarScores: {
      grammar: 92,
      spelling: 95,
      formatting: 88,
      overall: 91,
    },
    skillGaps: [
      {
        category: "DevOps",
        skills: ["Docker", "Kubernetes", "Jenkins", "GitHub Actions"],
      },
      {
        category: "Testing",
        skills: ["Jest", "Cypress", "Test-Driven Development"],
      },
      {
        category: "API Technologies",
        skills: ["GraphQL", "WebSockets", "gRPC"],
      },
    ],
    improvements: [
      {
        title: "Add Quantifiable Achievements",
        description: "Include specific metrics and numbers to demonstrate impact (e.g., '30% performance improvement').",
      },
      {
        title: "Highlight Leadership Experience",
        description: "Emphasize team leadership, mentoring, or project management responsibilities.",
      },
      {
        title: "Include Certifications",
        description: "Add relevant AWS, Azure, or other professional certifications if available.",
      },
    ],
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#f8fafc] to-white">
      {/* Breadcrumb */}
      <div className="bg-white border-b border-[#e2e8f0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-sm text-[#64748b]">
            Home <span className="mx-2">/</span> <span className="text-[#1e293b]">Analyzer</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="font-bold text-4xl md:text-5xl text-[#1e293b] mb-4">
            📊 Resume Analyzer
          </h1>
          <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
            Upload your resume and job description to get instant ATS optimization insights
          </p>
        </motion.div>

        {/* Analysis Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="mb-8 bg-gradient-to-br from-white to-[#f8fafc]">
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Job Description */}
              <div>
                <label className="block font-semibold text-[#1e293b] mb-3">
                  Job Description
                </label>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  className="w-full h-48 px-4 py-3 bg-white border border-[#e2e8f0] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#6366f1] focus:border-transparent resize-none"
                />
              </div>

              {/* Upload Resume */}
              <div>
                <label className="block font-semibold text-[#1e293b] mb-3">Upload Resume</label>
                <div className="h-48 border-2 border-dashed border-[#e2e8f0] rounded-lg hover:border-[#6366f1] transition-colors">
                  <label className="h-full flex flex-col items-center justify-center cursor-pointer">
                    <FileUp
                      className={`w-12 h-12 mb-3 ${
                        uploadedFile ? "text-[#10b981]" : "text-[#64748b]"
                      }`}
                    />
                    <span className="text-sm font-medium text-[#1e293b] mb-1">
                      {uploadedFile ? uploadedFile.name : "Click to upload PDF"}
                    </span>
                    <span className="text-xs text-[#64748b]">
                      {uploadedFile ? "File ready for analysis" : "PDF format only"}
                    </span>
                    <input
                      type="file"
                      accept=".pdf"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <Button
              onClick={handleAnalyze}
              disabled={!jobDescription || !uploadedFile || analyzing}
              size="lg"
              className="w-full"
            >
              {analyzing ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="mr-2"
                  >
                    <Sparkles className="w-5 h-5" />
                  </motion.div>
                  Analyzing...
                </>
              ) : (
                "🚀 Analyze Resume (Takes ~5 seconds)"
              )}
            </Button>
          </Card>
        </motion.div>

        {/* Processing Checklist */}
        <AnimatePresence>
          {analyzing && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-8"
            >
              <Card>
                <h3 className="font-semibold text-lg text-[#1e293b] mb-4">Processing...</h3>
                <div className="space-y-3">
                  {analysisSteps.map((step, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0.4 }}
                      animate={{
                        opacity: index <= analysisStep ? 1 : 0.4,
                      }}
                      className="flex items-center gap-3"
                    >
                      <CheckCircle2
                        className={`w-5 h-5 ${
                          index <= analysisStep ? "text-[#10b981]" : "text-[#cbd5e1]"
                        }`}
                      />
                      <span
                        className={`text-sm ${
                          index <= analysisStep ? "text-[#1e293b]" : "text-[#94a3b8]"
                        }`}
                      >
                        {step}
                      </span>
                    </motion.div>
                  ))}
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results Section */}
        <AnimatePresence>
          {showResults && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              {/* Score and Analysis Cards */}
              <div className="grid lg:grid-cols-2 gap-8 mb-8">
                {/* Score Card */}
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.2 }}
                >
                  <Card className="h-full">
                    <div className="flex flex-col items-center">
                      <ScoreGauge score={mockResults.score} size={180} />
                      <Badge variant="primary" className="mt-6 text-base px-6 py-2">
                        <Award className="w-4 h-4 mr-2" />
                        Strong Match
                      </Badge>

                      <div className="w-full mt-8 space-y-3">
                        <h4 className="font-semibold text-[#1e293b]">Processing Checklist</h4>
                        {analysisSteps.map((step, index) => (
                          <div key={index} className="flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-[#10b981]" />
                            <span className="text-sm text-[#64748b]">{step}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </Card>
                </motion.div>

                {/* Detailed Analysis */}
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  className="space-y-6"
                >
                  {/* Extracted Skills */}
                  <Card>
                    <h3 className="font-semibold text-lg text-[#1e293b] mb-4">Extracted Skills</h3>
                    <div className="flex flex-wrap gap-2">
                      {mockResults.extractedSkills.map((skill, index) => (
                        <Badge key={index} variant="primary">
                          {skill}
                        </Badge>
                      ))}
                    </div>
                  </Card>

                  {/* Matched Requirements */}
                  <Card>
                    <h3 className="font-semibold text-lg text-[#1e293b] mb-4">
                      Matched Requirements
                    </h3>
                    <ul className="space-y-2">
                      {mockResults.matchedRequirements.map((req, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <CheckCircle2 className="w-5 h-5 text-[#10b981] flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-[#64748b]">{req}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>

                  {/* Missing Skills */}
                  <Card>
                    <h3 className="font-semibold text-lg text-[#1e293b] mb-4">Missing Skills</h3>
                    <ul className="space-y-2">
                      {mockResults.missingSkills.map((skill, index) => (
                        <li key={index} className="flex items-start gap-2">
                          <AlertTriangle className="w-5 h-5 text-[#f59e0b] flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-[#64748b]">{skill}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>
                </motion.div>
              </div>

              {/* Score Breakdown */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <Card className="mb-8">
                  <h3 className="font-semibold text-lg text-[#1e293b] mb-6">Score Breakdown</h3>
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="text-center p-4 bg-[#f8fafc] rounded-lg">
                      <div className="text-3xl font-bold text-[#6366f1] mb-2">
                        {mockResults.percentile}%
                      </div>
                      <div className="text-sm text-[#64748b]">Percentile Ranking</div>
                    </div>
                    <div className="text-center p-4 bg-[#f8fafc] rounded-lg">
                      <div className="text-3xl font-bold text-[#8b5cf6] mb-2">
                        {mockResults.industryAverage}%
                      </div>
                      <div className="text-sm text-[#64748b]">Industry Average</div>
                    </div>
                    <div className="text-center p-4 bg-gradient-to-r from-[#10b981]/10 to-[#0ea5e9]/10 rounded-lg">
                      <div className="text-3xl font-bold text-[#10b981] mb-2">
                        +{mockResults.percentile - mockResults.industryAverage}%
                      </div>
                      <div className="text-sm text-[#64748b]">Above Average</div>
                    </div>
                  </div>
                </Card>
              </motion.div>

              {/* Grammar & Quality Check */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Card className="mb-8">
                  <h3 className="font-semibold text-lg text-[#1e293b] mb-6">
                    Grammar & Quality Check
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                      <Badge variant="primary" className="text-lg px-4 py-2 w-full">
                        {mockResults.grammarScores.grammar}%
                      </Badge>
                      <div className="text-sm text-[#64748b] mt-2">Grammar</div>
                    </div>
                    <div className="text-center">
                      <Badge variant="secondary" className="text-lg px-4 py-2 w-full">
                        {mockResults.grammarScores.spelling}%
                      </Badge>
                      <div className="text-sm text-[#64748b] mt-2">Spelling</div>
                    </div>
                    <div className="text-center">
                      <Badge variant="warning" className="text-lg px-4 py-2 w-full">
                        {mockResults.grammarScores.formatting}%
                      </Badge>
                      <div className="text-sm text-[#64748b] mt-2">Formatting</div>
                    </div>
                    <div className="text-center">
                      <div className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] text-white text-lg px-4 py-2 rounded-full font-medium w-full">
                        {mockResults.grammarScores.overall}%
                      </div>
                      <div className="text-sm text-[#64748b] mt-2">Overall Quality</div>
                    </div>
                  </div>
                </Card>
              </motion.div>

              {/* Skill Gaps */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
              >
                <h3 className="font-semibold text-xl text-[#1e293b] mb-6">Skill Gaps</h3>
                <div className="grid md:grid-cols-3 gap-6 mb-8">
                  {mockResults.skillGaps.map((gap, index) => (
                    <Card key={index}>
                      <h4 className="font-semibold text-[#1e293b] mb-4">{gap.category}</h4>
                      <div className="space-y-2">
                        {gap.skills.map((skill, skillIndex) => (
                          <div key={skillIndex} className="flex items-center gap-2">
                            <div className="w-2 h-2 bg-[#6366f1] rounded-full" />
                            <span className="text-sm text-[#64748b]">{skill}</span>
                          </div>
                        ))}
                      </div>
                    </Card>
                  ))}
                </div>
              </motion.div>

              {/* Improvement Suggestions */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
              >
                <h3 className="font-semibold text-xl text-[#1e293b] mb-6">
                  Improvement Suggestions
                </h3>
                <div className="space-y-4 mb-8">
                  {mockResults.improvements.map((improvement, index) => (
                    <Card key={index} className="flex items-start gap-4">
                      <div className="w-10 h-10 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-lg flex items-center justify-center flex-shrink-0">
                        <TrendingUp className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex-1">
                        <h4 className="font-semibold text-[#1e293b] mb-2">{improvement.title}</h4>
                        <p className="text-sm text-[#64748b]">{improvement.description}</p>
                      </div>
                    </Card>
                  ))}
                </div>
              </motion.div>

              {/* Export Section */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 }}
              >
                <Card className="bg-gradient-to-r from-[#f8fafc] to-white">
                  <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                      <h3 className="font-semibold text-lg text-[#1e293b] mb-2">
                        Export Your Analysis
                      </h3>
                      <p className="text-sm text-[#64748b]">
                        Download your complete analysis report in your preferred format
                      </p>
                    </div>
                    <div className="flex gap-4">
                      <Button variant="outline">
                        <Download className="w-4 h-4 mr-2" />
                        Export CSV
                      </Button>
                      <Button>
                        <Download className="w-4 h-4 mr-2" />
                        Export PDF
                      </Button>
                    </div>
                  </div>
                </Card>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
