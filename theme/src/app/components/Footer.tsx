import { Link } from "react-router";
import { FileText, Twitter, Linkedin, Github } from "lucide-react";

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-[#1e293b] text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-6 h-6 text-[#6366f1]" />
              <span className="font-bold text-xl">AI Resume Pro</span>
            </div>
            <p className="text-[#94a3b8] mb-4">
              Transform your resume into an ATS winner with AI-powered analysis and optimization.
            </p>
            <div className="flex gap-4">
              <a
                href="#"
                className="w-10 h-10 flex items-center justify-center rounded-full bg-[#334155] hover:bg-[#6366f1] transition-colors"
              >
                <Twitter className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 flex items-center justify-center rounded-full bg-[#334155] hover:bg-[#6366f1] transition-colors"
              >
                <Linkedin className="w-5 h-5" />
              </a>
              <a
                href="#"
                className="w-10 h-10 flex items-center justify-center rounded-full bg-[#334155] hover:bg-[#6366f1] transition-colors"
              >
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-[#94a3b8] hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/analyzer" className="text-[#94a3b8] hover:text-white transition-colors">
                  Analyzer
                </Link>
              </li>
              <li>
                <Link to="/template" className="text-[#94a3b8] hover:text-white transition-colors">
                  Template
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-[#94a3b8] hover:text-white transition-colors">
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-[#94a3b8] hover:text-white transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" className="text-[#94a3b8] hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-[#94a3b8] hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="#" className="text-[#94a3b8] hover:text-white transition-colors">
                  Contact Us
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-[#334155] text-center text-[#94a3b8] text-sm">
          © {currentYear} AI Resume Pro. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
