import { Target, Zap, Brain, Users, CheckCircle2 } from "lucide-react";
import { motion } from "motion/react";
import { Link } from "react-router";
import { Button } from "../components/Button";
import { Card } from "../components/Card";

export function About() {
  const mission = {
    title: "Our Mission",
    description:
      "We believe everyone deserves a fair chance in the job market. Our AI-powered platform democratizes access to professional resume optimization, helping job seekers overcome ATS barriers and showcase their true potential.",
  };

  const howItWorks = [
    {
      step: "1",
      title: "Upload & Analyze",
      description: "Submit your resume and job description for instant AI-powered analysis.",
    },
    {
      step: "2",
      title: "Get Insights",
      description: "Receive detailed ATS score, skill gaps, and matched requirements.",
    },
    {
      step: "3",
      title: "Optimize Content",
      description: "Use AI-generated templates and suggestions to improve your resume.",
    },
    {
      step: "4",
      title: "Land Interviews",
      description: "Apply with confidence knowing your resume is optimized for success.",
    },
  ];

  const technology = [
    {
      icon: Brain,
      title: "Advanced NLP",
      description: "Natural language processing to understand job requirements and resume content.",
    },
    {
      icon: Zap,
      title: "Real-time Analysis",
      description: "Lightning-fast processing with results in under 5 seconds.",
    },
    {
      icon: Target,
      title: "ATS Optimization",
      description: "Trained on thousands of successful resumes across industries.",
    },
    {
      icon: Users,
      title: "User-Centric Design",
      description: "Intuitive interface designed for job seekers of all backgrounds.",
    },
  ];

  const features = [
    "ATS score calculation with industry benchmarks",
    "Skill extraction and gap analysis",
    "Grammar and formatting checks",
    "AI-powered resume template generation",
    "Export to CSV and PDF formats",
    "Real-time processing and feedback",
    "Privacy-focused data handling",
    "24/7 availability and support",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#f8fafc] to-white">
      {/* Breadcrumb */}
      <div className="bg-white border-b border-[#e2e8f0]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-sm text-[#64748b]">
            Home <span className="mx-2">/</span> <span className="text-[#1e293b]">About</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="font-bold text-4xl md:text-5xl text-[#1e293b] mb-4">
            About AI Resume Pro
          </h1>
          <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
            Empowering job seekers with AI-driven resume optimization
          </p>
        </motion.div>

        {/* Our Mission */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-16"
        >
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="font-bold text-3xl md:text-4xl text-[#1e293b] mb-6">
                {mission.title}
              </h2>
              <p className="text-lg text-[#64748b] leading-relaxed mb-6">{mission.description}</p>
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-full flex items-center justify-center">
                  <Target className="w-8 h-8 text-white" />
                </div>
                <div>
                  <div className="font-bold text-2xl text-[#1e293b]">10,000+</div>
                  <div className="text-sm text-[#64748b]">Resumes optimized</div>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1758599543131-d69eb265a5cd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMGNhcmVlciUyMHN1Y2Nlc3MlMjB0ZWFtd29ya3xlbnwxfHx8fDE3NzU4ODE3NjF8MA&ixlib=rb-4.1.0&q=80&w=1080"
                  alt="Team collaboration"
                  className="w-full h-[400px] object-cover"
                />
              </div>
            </div>
          </div>
        </motion.div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="font-bold text-3xl md:text-4xl text-[#1e293b] mb-4">How It Works</h2>
            <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
              Four simple steps to transform your resume
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {howItWorks.map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="h-full text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl font-bold">
                    {step.step}
                  </div>
                  <h3 className="font-semibold text-lg text-[#1e293b] mb-3">{step.title}</h3>
                  <p className="text-sm text-[#64748b]">{step.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-16"
        >
          <div className="text-center mb-12">
            <h2 className="font-bold text-3xl md:text-4xl text-[#1e293b] mb-4">
              Powered by Advanced AI
            </h2>
            <p className="text-lg text-[#64748b] max-w-2xl mx-auto">
              Cutting-edge technology delivering accurate and actionable insights
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {technology.map((tech, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="h-full hover:scale-105 transition-transform">
                  <div className="w-12 h-12 bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-lg flex items-center justify-center mb-4">
                    <tech.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-semibold text-[#1e293b] mb-2">{tech.title}</h3>
                  <p className="text-sm text-[#64748b]">{tech.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Features Highlight */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="relative order-2 lg:order-1">
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1759593218431-6f1585bc14de?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwcm9mZXNzaW9uYWwlMjBvZmZpY2UlMjB3b3Jrc3BhY2UlMjBkZXNrJTIwbGFwdG9wfGVufDF8fHx8MTc3NTg4MTc2MHww&ixlib=rb-4.1.0&q=80&w=1080"
                  alt="Professional workspace"
                  className="w-full h-[400px] object-cover"
                />
              </div>
            </div>
            <div className="order-1 lg:order-2">
              <h2 className="font-bold text-3xl md:text-4xl text-[#1e293b] mb-6">
                Everything You Need
              </h2>
              <div className="grid grid-cols-1 gap-3">
                {features.map((feature, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.05 }}
                    className="flex items-center gap-3"
                  >
                    <CheckCircle2 className="w-5 h-5 text-[#10b981] flex-shrink-0" />
                    <span className="text-[#64748b]">{feature}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Company Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mb-16"
        >
          <Card className="bg-gradient-to-br from-[#f8fafc] to-white">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-semibold text-xl text-[#1e293b] mb-4">Who We Are</h3>
                <p className="text-[#64748b] mb-4">
                  AI Resume Pro was founded in 2024 by a team of career coaches, software engineers,
                  and AI researchers who recognized the challenges job seekers face with automated
                  applicant tracking systems.
                </p>
                <p className="text-[#64748b]">
                  Our diverse team brings together expertise in machine learning, human resources,
                  and user experience design to create tools that truly make a difference in
                  people's careers.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-xl text-[#1e293b] mb-4">Our Commitment</h3>
                <p className="text-[#64748b] mb-4">
                  We're committed to privacy, accuracy, and continuous improvement. Your resume data
                  is processed in real-time and never stored permanently.
                </p>
                <p className="text-[#64748b]">
                  We regularly update our AI models based on the latest hiring trends and ATS
                  algorithms to ensure you get the most accurate and relevant feedback.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <div className="text-center bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] rounded-2xl p-12">
            <h2 className="font-bold text-3xl md:text-4xl text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-lg text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of job seekers who have transformed their resumes with AI Resume Pro
            </p>
            <Link to="/analyzer">
              <Button variant="secondary" size="lg" className="bg-white text-[#6366f1]">
                Try It Free
              </Button>
            </Link>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
