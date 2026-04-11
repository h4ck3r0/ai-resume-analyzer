import { useState } from "react";
import { Sparkles, Copy, Download, CheckCircle2 } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import { Button } from "../components/Button";
import { Card } from "../components/Card";

export function TemplateGenerator() {
  const [jobDescription, setJobDescription] = useState("");
  const [generating, setGenerating] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const benefits = [
    { title: "AI-Powered", description: "Intelligent content generation" },
    { title: "Tailored", description: "Customized to job requirements" },
    { title: "Professional", description: "Industry-standard formatting" },
    { title: "Ready to Use", description: "Copy and paste immediately" },
  ];

  const handleGenerate = () => {
    setGenerating(true);
    setTimeout(() => {
      setGenerating(false);
      setShowResults(true);
    }, 3000);
  };

  const handleCopy = (section: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(section);
    setTimeout(() => setCopied(null), 2000);
  };

  const mockResults = {
    professionalSummary:
      "Results-driven Senior Software Engineer with 8+ years of experience building scalable web applications and leading cross-functional teams. Expertise in JavaScript, React, and cloud infrastructure with a proven track record of delivering high-impact solutions that drive business growth. Passionate about code quality, mentorship, and leveraging cutting-edge technologies to solve complex problems.",
    keySections: [
      "Professional Summary",
      "Technical Skills",
      "Work Experience",
      "Notable Projects",
      "Education & Certifications",
      "Leadership & Awards",
    ],
    achievementBullets: [
      "Architected and deployed microservices platform serving 2M+ daily users, reducing API latency by 45%",
      "Led team of 6 engineers in migrating legacy monolith to React, improving development velocity by 60%",
      "Implemented automated CI/CD pipeline reducing deployment time from 2 hours to 15 minutes",
      "Mentored 10+ junior developers, with 80% receiving promotions within 18 months",
      "Optimized database queries and caching strategy, cutting infrastructure costs by $120K annually",
    ],
    howToUse: [
      "Review the generated summary and customize with your specific achievements",
      "Organize your resume using the recommended key sections",
      "Adapt the achievement bullets to match your experience using the STAR method",
      "Ensure all content is truthful and accurately represents your background",
      "Use action verbs and quantifiable metrics throughout",
    ],
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#f8fafc] to-white">
      {/* Breadcrumb */}
      <div className="bg-white border-b border-[#e2e8f0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-sm text-[#64748b]">
            Home <span className="mx-2">/</span> <span className="text-[#1e293b]">Template</span>
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
            ✨ Resume Template Generator
          </h1>
          <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
            Generate AI-powered resume templates tailored to your target job description
          </p>
        </motion.div>

        {/* Benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12"
        >
          {benefits.map((benefit, index) => (
            <Card key={index} className="text-center">
              <div className="font-semibold text-[#1e293b] mb-1">{benefit.title}</div>
              <div className="text-sm text-[#64748b]">{benefit.description}</div>
            </Card>
          ))}
        </motion.div>

        {/* Generator Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card className="mb-8 bg-gradient-to-br from-white to-[#f8fafc]">
            <label className="block font-semibold text-[#1e293b] mb-4">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description to generate a tailored resume template..."
              className="w-full h-48 px-4 py-3 bg-white border border-[#e2e8f0] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#6366f1] focus:border-transparent resize-none mb-6"
            />
            <Button
              onClick={handleGenerate}
              disabled={!jobDescription || generating}
              size="lg"
              className="w-full"
            >
              {generating ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="mr-2"
                  >
                    <Sparkles className="w-5 h-5" />
                  </motion.div>
                  Generating Template...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 mr-2" />
                  Generate Template
                </>
              )}
            </Button>
          </Card>
        </motion.div>

        {/* Results */}
        <AnimatePresence>
          {showResults && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <div className="grid lg:grid-cols-3 gap-8">
                {/* Left Column */}
                <div className="lg:col-span-2 space-y-6">
                  {/* Professional Summary */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                  >
                    <Card variant="gradient-border" gradientColor="yellow">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-lg text-[#1e293b]">
                          Professional Summary
                        </h3>
                        <button
                          onClick={() =>
                            handleCopy("summary", mockResults.professionalSummary)
                          }
                          className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[#f8fafc] hover:bg-[#f1f5f9] rounded-lg transition-colors"
                        >
                          {copied === "summary" ? (
                            <>
                              <CheckCircle2 className="w-4 h-4 text-[#10b981]" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="w-4 h-4" />
                              Copy
                            </>
                          )}
                        </button>
                      </div>
                      <p className="text-[#64748b] leading-relaxed">
                        {mockResults.professionalSummary}
                      </p>
                    </Card>
                  </motion.div>

                  {/* Key Sections */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                  >
                    <Card variant="gradient-border" gradientColor="blue">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-lg text-[#1e293b]">
                          Recommended Resume Sections
                        </h3>
                        <button
                          onClick={() =>
                            handleCopy("sections", mockResults.keySections.join("\n"))
                          }
                          className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[#f8fafc] hover:bg-[#f1f5f9] rounded-lg transition-colors"
                        >
                          {copied === "sections" ? (
                            <>
                              <CheckCircle2 className="w-4 h-4 text-[#10b981]" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="w-4 h-4" />
                              Copy
                            </>
                          )}
                        </button>
                      </div>
                      <ol className="space-y-2">
                        {mockResults.keySections.map((section, index) => (
                          <li key={index} className="flex items-center gap-3">
                            <div className="w-7 h-7 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-full flex items-center justify-center text-white text-sm font-semibold flex-shrink-0">
                              {index + 1}
                            </div>
                            <span className="text-[#64748b]">{section}</span>
                          </li>
                        ))}
                      </ol>
                    </Card>
                  </motion.div>

                  {/* Achievement Bullets */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                  >
                    <Card variant="gradient-border" gradientColor="green">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-lg text-[#1e293b]">
                          Sample Achievement Bullets
                        </h3>
                        <button
                          onClick={() =>
                            handleCopy("bullets", mockResults.achievementBullets.join("\n• "))
                          }
                          className="flex items-center gap-2 px-3 py-1.5 text-sm bg-[#f8fafc] hover:bg-[#f1f5f9] rounded-lg transition-colors"
                        >
                          {copied === "bullets" ? (
                            <>
                              <CheckCircle2 className="w-4 h-4 text-[#10b981]" />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="w-4 h-4" />
                              Copy
                            </>
                          )}
                        </button>
                      </div>
                      <ul className="space-y-3">
                        {mockResults.achievementBullets.map((bullet, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <div className="w-1.5 h-1.5 bg-[#10b981] rounded-full flex-shrink-0 mt-2" />
                            <span className="text-[#64748b] text-sm leading-relaxed">
                              {bullet}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </Card>
                  </motion.div>
                </div>

                {/* Right Column */}
                <div className="space-y-6">
                  {/* How to Use */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                  >
                    <Card className="bg-gradient-to-br from-[#0ea5e9]/5 to-[#06b6d4]/5 border-2 border-[#0ea5e9]/20 sticky top-24">
                      <h3 className="font-semibold text-lg text-[#1e293b] mb-4">How to Use</h3>
                      <ol className="space-y-3">
                        {mockResults.howToUse.map((step, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <div className="w-6 h-6 bg-[#0ea5e9] rounded-full flex items-center justify-center text-white text-xs font-semibold flex-shrink-0 mt-0.5">
                              {index + 1}
                            </div>
                            <span className="text-sm text-[#64748b]">{step}</span>
                          </li>
                        ))}
                      </ol>

                      <div className="mt-6 pt-6 border-t border-[#e2e8f0]">
                        <div className="flex flex-col gap-3">
                          <Button variant="outline" className="w-full">
                            <Download className="w-4 h-4 mr-2" />
                            Export as PDF
                          </Button>
                          <Button className="w-full">
                            <Copy className="w-4 h-4 mr-2" />
                            Copy All
                          </Button>
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
