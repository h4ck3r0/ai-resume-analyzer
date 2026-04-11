import { Link } from "react-router";
import {
  FileSearch,
  Sparkles,
  Download,
  CheckCircle2,
  TrendingUp,
  Clock,
  HeadphonesIcon,
  ChevronDown,
} from "lucide-react";
import { motion } from "motion/react";
import { Button } from "../components/Button";
import { Card } from "../components/Card";
import { useState } from "react";

export function Home() {
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const stats = [
    { value: "10,000+", label: "Resumes Analyzed" },
    { value: "89%", label: "Average Match" },
    { value: "2 Min", label: "Average Time" },
    { value: "24/7", label: "Support" },
  ];

  const features = [
    {
      icon: FileSearch,
      title: "Resume Analyzer",
      description: "Get instant ATS score and detailed analysis of your resume against job requirements.",
    },
    {
      icon: Sparkles,
      title: "Template Generator",
      description: "AI-powered templates tailored to your target job with professional formatting.",
    },
    {
      icon: Download,
      title: "Export Options",
      description: "Export your analysis and templates as CSV or PDF for easy sharing.",
    },
  ];

  const faqs = [
    {
      question: "What is an ATS score?",
      answer:
        "ATS (Applicant Tracking System) score measures how well your resume matches job requirements and can be parsed by automated systems used by employers.",
    },
    {
      question: "How accurate is the AI analysis?",
      answer:
        "Our AI achieves 89% average match accuracy by analyzing thousands of successful resumes and job postings across various industries.",
    },
    {
      question: "Is my resume data secure?",
      answer:
        "Absolutely. We use enterprise-grade encryption and never store your resume data permanently. All analysis is done in real-time and deleted after processing.",
    },
    {
      question: "Can I analyze multiple resumes?",
      answer:
        "Yes! You can analyze as many resumes as you need. Each analysis takes approximately 2 minutes to complete.",
    },
    {
      question: "What file formats are supported?",
      answer:
        "We currently support PDF format for resume uploads. This ensures the best accuracy in our analysis.",
    },
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-[#f8fafc] via-white to-[#f1f5f9]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left: Text Content */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="font-extrabold text-[#1e293b] leading-tight mb-6">
                <span className="block text-4xl md:text-6xl">Transform Your Resume</span>
                <span className="block text-4xl md:text-6xl bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] bg-clip-text text-transparent">
                  into an ATS Winner
                </span>
              </h1>
              <p className="text-lg md:text-xl text-[#64748b] mb-8 max-w-xl">
                Leverage AI-powered analysis to optimize your resume for Applicant Tracking Systems and
                land more interviews.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/analyzer">
                  <Button size="lg" className="w-full sm:w-auto">
                    Get Started Free
                  </Button>
                </Link>
                <Link to="/about">
                  <Button variant="outline" size="lg" className="w-full sm:w-auto">
                    Learn More
                  </Button>
                </Link>
              </div>
            </motion.div>

            {/* Right: Hero Image */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1765648684555-de2d0f6af467?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwzfHxwcm9mZXNzaW9uYWwlMjBvZmZpY2UlMjB3b3Jrc3BhY2UlMjBkZXNrJTIwbGFwdG9wfGVufDF8fHx8MTc3NTg4MTc2MHww&ixlib=rb-4.1.0&q=80&w=1080"
                  alt="Professional working on resume"
                  className="w-full h-[400px] md:h-[500px] object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
              </div>
              {/* Floating stats card */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.5 }}
                className="absolute bottom-6 left-6 right-6 bg-white/95 backdrop-blur-sm rounded-xl p-4 shadow-lg"
              >
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-full flex items-center justify-center">
                    <TrendingUp className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="font-bold text-lg text-[#1e293b]">89% Success Rate</div>
                    <div className="text-sm text-[#64748b]">Users landing interviews</div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white border-y border-[#e2e8f0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="font-extrabold text-3xl md:text-4xl bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-sm md:text-base text-[#64748b]">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 md:py-24 bg-gradient-to-b from-white to-[#f8fafc]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="font-bold text-3xl md:text-5xl text-[#1e293b] mb-4">
              Everything You Need to Succeed
            </h2>
            <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
              Powerful AI tools to transform your resume and maximize your interview opportunities.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card className="h-full hover:scale-105 transition-transform">
                  <div className="w-14 h-14 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-xl flex items-center justify-center mb-6">
                    <feature.icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="font-bold text-xl text-[#1e293b] mb-3">{feature.title}</h3>
                  <p className="text-[#64748b]">{feature.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 md:py-24 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="font-bold text-3xl md:text-5xl text-[#1e293b] mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-lg text-[#64748b]">Everything you need to know about AI Resume Pro</p>
          </motion.div>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
              >
                <button
                  onClick={() => setOpenFaq(openFaq === index ? null : index)}
                  className="w-full text-left bg-[#f8fafc] hover:bg-[#f1f5f9] rounded-xl p-6 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-lg text-[#1e293b] pr-4">{faq.question}</h3>
                    <ChevronDown
                      className={`w-5 h-5 text-[#64748b] transition-transform flex-shrink-0 ${
                        openFaq === index ? "rotate-180" : ""
                      }`}
                    />
                  </div>
                  <motion.div
                    initial={false}
                    animate={{
                      height: openFaq === index ? "auto" : 0,
                      opacity: openFaq === index ? 1 : 0,
                    }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <p className="text-[#64748b] mt-4">{faq.answer}</p>
                  </motion.div>
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6]">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-bold text-3xl md:text-5xl text-white mb-6">
              Ready to Transform Your Resume?
            </h2>
            <p className="text-lg md:text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of job seekers who have improved their resumes and landed more interviews.
            </p>
            <Link to="/analyzer">
              <Button
                variant="secondary"
                size="lg"
                className="bg-white text-[#6366f1] hover:bg-[#f8fafc]"
              >
                Start Free Analysis
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
