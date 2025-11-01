#!/usr/bin/env python3
"""
Generate Real-World Cost Scenarios and Examples
Creates comprehensive usage scenarios with detailed cost analysis and recommendations.
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from cost_calculator import FrameworkCostCalculator, Framework, ModelProvider

class ScenarioGenerator:
    """Generate comprehensive cost scenarios for different business use cases"""
    
    def __init__(self):
        self.calculator = FrameworkCostCalculator()
        
        # Define business scenarios with realistic parameters
        self.scenarios = {
            "startup_mvp": {
                "name": "Startup MVP",
                "description": "Early-stage startup building minimum viable product",
                "requests_per_month": 1000,
                "model": ModelProvider.OPENAI_GPT4O_MINI,
                "custom_tokens": 800,
                "business_context": {
                    "team_size": "2-5 developers",
                    "budget": "Limited seed funding",
                    "timeline": "3-6 months to market",
                    "priorities": ["Cost efficiency", "Speed to market", "Simplicity"]
                }
            },
            
            "saas_growth": {
                "name": "SaaS Growth Stage",
                "description": "Growing SaaS company scaling user base",
                "requests_per_month": 25000,
                "model": ModelProvider.OPENAI_GPT4O,
                "custom_tokens": 1200,
                "business_context": {
                    "team_size": "10-20 developers",
                    "budget": "Series A funded",
                    "timeline": "12-18 months scaling",
                    "priorities": ["Scalability", "Performance", "Feature velocity"]
                }
            },
            
            "enterprise_deployment": {
                "name": "Enterprise Deployment",
                "description": "Large enterprise with compliance requirements",
                "requests_per_month": 100000,
                "model": ModelProvider.CLAUDE_35_SONNET,
                "custom_tokens": 2000,
                "business_context": {
                    "team_size": "50+ developers",
                    "budget": "Enterprise budget",
                    "timeline": "Multi-year deployment",
                    "priorities": ["Security", "Compliance", "Reliability", "Support"]
                }
            },
            
            "ai_research_lab": {
                "name": "AI Research Lab",
                "description": "Research institution exploring AI capabilities",
                "requests_per_month": 15000,
                "model": ModelProvider.OPENAI_GPT4O,
                "custom_tokens": 3000,
                "business_context": {
                    "team_size": "5-15 researchers",
                    "budget": "Grant funding",
                    "timeline": "1-3 year projects",
                    "priorities": ["Experimental features", "Flexibility", "Research capabilities"]
                }
            },
            
            "ecommerce_platform": {
                "name": "E-commerce Platform",
                "description": "Online retail platform with AI-powered features",
                "requests_per_month": 75000,
                "model": ModelProvider.OPENAI_GPT4O,
                "custom_tokens": 1500,
                "business_context": {
                    "team_size": "20-40 developers",
                    "budget": "Revenue-funded growth",
                    "timeline": "Continuous deployment",
                    "priorities": ["Customer experience", "Conversion rates", "Cost optimization"]
                }
            },
            
            "healthcare_startup": {
                "name": "Healthcare AI Startup",
                "description": "Digital health company with AI diagnostics",
                "requests_per_month": 8000,
                "model": ModelProvider.CLAUDE_35_SONNET,
                "custom_tokens": 2500,
                "business_context": {
                    "team_size": "10-25 developers",
                    "budget": "Series A/B funding",
                    "timeline": "18-24 months to regulatory approval",
                    "priorities": ["Regulatory compliance", "Accuracy", "Privacy", "Auditability"]
                }
            },
            
            "fintech_robo_advisor": {
                "name": "FinTech Robo-Advisor",
                "description": "Automated investment platform with AI recommendations",
                "requests_per_month": 45000,
                "model": ModelProvider.OPENAI_GPT4O,
                "custom_tokens": 1800,
                "business_context": {
                    "team_size": "15-30 developers",
                    "budget": "Well-funded growth stage",
                    "timeline": "Continuous optimization",
                    "priorities": ["Regulatory compliance", "Performance", "Risk management", "Cost efficiency"]
                }
            },
            
            "content_creation_platform": {
                "name": "Content Creation Platform",
                "description": "AI-powered content generation for marketing teams",
                "requests_per_month": 35000,
                "model": ModelProvider.OPENAI_GPT4O,
                "custom_tokens": 2200,
                "business_context": {
                    "team_size": "8-20 developers",
                    "budget": "Bootstrap/Series A",
                    "timeline": "6-12 months to profitability",
                    "priorities": ["Content quality", "Speed", "Cost per output", "Scalability"]
                }
            }
        }
    
    def generate_scenario_analysis(self, scenario_key: str) -> Dict[str, Any]:
        """Generate comprehensive analysis for a specific scenario"""
        scenario = self.scenarios[scenario_key]
        
        # Calculate costs for all frameworks
        comparison = self.calculator.compare_frameworks(
            scenario["model"],
            scenario["requests_per_month"],
            scenario["custom_tokens"]
        )
        
        # Find best options
        sorted_frameworks = sorted(comparison.items(), key=lambda x: x[1]["total_cost"])
        best_framework = sorted_frameworks[0]
        most_expensive = sorted_frameworks[-1]
        
        # Calculate potential savings
        max_savings = most_expensive[1]["total_cost"] - best_framework[1]["total_cost"]
        max_annual_savings = max_savings * 12
        
        # Generate framework recommendations
        recommendations = self._generate_recommendations(scenario, comparison)
        
        # Calculate ROI scenarios
        roi_analysis = self._calculate_roi_scenarios(scenario, comparison)
        
        # Convert ModelProvider enum to string for JSON serialization
        scenario_data = scenario.copy()
        scenario_data["model"] = scenario["model"].value
        
        return {
            "scenario": scenario_data,
            "framework_comparison": comparison,
            "cost_summary": {
                "best_option": best_framework[0],
                "best_monthly_cost": best_framework[1]["total_cost"],
                "most_expensive": most_expensive[0],
                "highest_monthly_cost": most_expensive[1]["total_cost"],
                "max_monthly_savings": max_savings,
                "max_annual_savings": max_annual_savings,
                "savings_percentage": (max_savings / most_expensive[1]["total_cost"]) * 100
            },
            "recommendations": recommendations,
            "roi_analysis": roi_analysis,
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, scenario: Dict, comparison: Dict) -> List[Dict]:
        """Generate framework-specific recommendations based on scenario"""
        recommendations = []
        
        # Sort frameworks by cost
        sorted_frameworks = sorted(comparison.items(), key=lambda x: x[1]["total_cost"])
        
        # Budget-conscious recommendation
        if scenario["requests_per_month"] < 10000:
            recommendations.append({
                "category": "Budget Optimization",
                "framework": sorted_frameworks[0][0],
                "reasoning": f"For {scenario['requests_per_month']:,} requests/month, {sorted_frameworks[0][1]['framework_name']} offers the best cost efficiency at ${sorted_frameworks[0][1]['total_cost']:.2f}/month",
                "priority": "high",
                "savings": f"${(sorted_frameworks[-1][1]['total_cost'] - sorted_frameworks[0][1]['total_cost']) * 12:.0f}/year vs most expensive option"
            })
        
        # Performance recommendation for high-volume scenarios
        if scenario["requests_per_month"] > 50000:
            # Find frameworks with good performance characteristics
            for fw_key, fw_data in comparison.items():
                if fw_key in ["semantic_kernel", "autogen"] and fw_data["total_cost"] < sorted_frameworks[-1][1]["total_cost"] * 1.2:
                    recommendations.append({
                        "category": "Performance & Scale",
                        "framework": fw_key,
                        "reasoning": f"{fw_data['framework_name']} offers excellent performance at scale with enterprise-grade reliability",
                        "priority": "medium",
                        "cost_premium": f"${fw_data['total_cost'] - sorted_frameworks[0][1]['total_cost']:.2f}/month premium for enhanced capabilities"
                    })
                    break
        
        # Enterprise recommendation
        if "enterprise" in scenario["name"].lower() or scenario["requests_per_month"] > 75000:
            recommendations.append({
                "category": "Enterprise Ready",
                "framework": "semantic_kernel",
                "reasoning": "Semantic Kernel provides enterprise integration, security features, and Microsoft ecosystem compatibility",
                "priority": "high",
                "enterprise_benefits": ["Native Azure integration", "Enterprise security", "Professional support", "Compliance features"]
            })
        
        # Research/experimental recommendation
        if "research" in scenario["name"].lower() or "startup" in scenario["name"].lower():
            recommendations.append({
                "category": "Innovation & Flexibility",
                "framework": "autogen",
                "reasoning": "AutoGen offers cutting-edge multi-agent capabilities and research-grade features for experimental use cases",
                "priority": "medium",
                "experimental_benefits": ["Multi-agent conversations", "Latest research features", "Flexible architectures", "Active development"]
            })
        
        return recommendations
    
    def _calculate_roi_scenarios(self, scenario: Dict, comparison: Dict) -> Dict:
        """Calculate ROI for different deployment scenarios"""
        sorted_frameworks = sorted(comparison.items(), key=lambda x: x[1]["total_cost"])
        best_framework = sorted_frameworks[0]
        
        # Calculate development cost scenarios
        development_costs = {
            "semantic_kernel": 25000,  # Lower due to enterprise tooling
            "autogen": 35000,         # Medium due to complexity
            "crewai": 30000,          # Medium complexity
            "langchain": 40000,       # Higher due to custom integration
            "langgraph": 45000        # Highest due to stateful complexity
        }
        
        roi_scenarios = {}
        
        for fw_key, fw_data in comparison.items():
            monthly_cost = fw_data["total_cost"]
            annual_cost = monthly_cost * 12
            dev_cost = development_costs.get(fw_key, 35000)
            
            # Calculate payback period comparing to best option
            if fw_key != best_framework[0]:
                annual_cost_diff = (monthly_cost - best_framework[1]["total_cost"]) * 12
                if annual_cost_diff > 0:
                    payback_months = dev_cost / annual_cost_diff if annual_cost_diff > 0 else float('inf')
                else:
                    payback_months = 0
            else:
                payback_months = 0
                annual_cost_diff = 0
            
            roi_scenarios[fw_key] = {
                "framework_name": fw_data["framework_name"],
                "development_cost": dev_cost,
                "annual_operating_cost": annual_cost,
                "total_first_year_cost": dev_cost + annual_cost,
                "annual_cost_vs_best": annual_cost_diff,
                "payback_period_months": payback_months if payback_months != float('inf') else None,
                "three_year_tco": dev_cost + (annual_cost * 3)
            }
        
        return roi_scenarios
    
    def generate_all_scenarios(self) -> Dict[str, Any]:
        """Generate analysis for all scenarios"""
        all_scenarios = {}
        
        for scenario_key in self.scenarios.keys():
            print(f"Generating analysis for: {self.scenarios[scenario_key]['name']}")
            all_scenarios[scenario_key] = self.generate_scenario_analysis(scenario_key)
        
        return {
            "scenarios": all_scenarios,
            "summary": self._generate_summary(all_scenarios),
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_summary(self, all_scenarios: Dict) -> Dict:
        """Generate summary insights across all scenarios"""
        framework_wins = {}
        total_scenarios = len(all_scenarios)
        
        for scenario_key, scenario_data in all_scenarios.items():
            best_framework = scenario_data["cost_summary"]["best_option"]
            framework_wins[best_framework] = framework_wins.get(best_framework, 0) + 1
        
        # Calculate average savings potential
        total_max_savings = sum(s["cost_summary"]["max_annual_savings"] for s in all_scenarios.values())
        avg_max_savings = total_max_savings / total_scenarios
        
        return {
            "framework_performance": {
                fw: {"wins": wins, "win_rate": wins/total_scenarios}
                for fw, wins in framework_wins.items()
            },
            "average_max_annual_savings": avg_max_savings,
            "key_insights": [
                f"Framework selection can save up to ${avg_max_savings:,.0f} annually on average",
                f"Semantic Kernel wins {framework_wins.get('semantic_kernel', 0)}/{total_scenarios} scenarios",
                f"AutoGen wins {framework_wins.get('autogen', 0)}/{total_scenarios} scenarios",
                "Cost optimization varies significantly by use case and scale"
            ]
        }

def main():
    """Generate comprehensive scenario analysis"""
    print("🎯 Generating Real-World Cost Scenarios...")
    
    generator = ScenarioGenerator()
    
    # Generate all scenarios
    all_scenarios = generator.generate_all_scenarios()
    
    # Save comprehensive analysis
    with open("cost_scenarios_analysis.json", "w") as f:
        json.dump(all_scenarios, f, indent=2)
    
    print(f"\n✅ Generated analysis for {len(all_scenarios['scenarios'])} scenarios:")
    
    # Display summary
    summary = all_scenarios["summary"]
    print(f"\n📊 Summary Insights:")
    for insight in summary["key_insights"]:
        print(f"   • {insight}")
    
    print(f"\n🏆 Framework Performance:")
    for fw, stats in summary["framework_performance"].items():
        win_rate = stats["win_rate"] * 100
        print(f"   • {fw.replace('_', ' ').title()}: {stats['wins']} wins ({win_rate:.1f}%)")
    
    print(f"\n💰 Average potential savings: ${summary['average_max_annual_savings']:,.0f}/year")
    
    # Generate sample scenario output
    sample_scenario = all_scenarios["scenarios"]["saas_growth"]
    print(f"\n📋 Sample Scenario: {sample_scenario['scenario']['name']}")
    print(f"   Best option: {sample_scenario['cost_summary']['best_option'].replace('_', ' ').title()}")
    print(f"   Monthly cost: ${sample_scenario['cost_summary']['best_monthly_cost']:.2f}")
    print(f"   Annual savings potential: ${sample_scenario['cost_summary']['max_annual_savings']:.0f}")
    
    print(f"\n🔗 Full analysis saved to: cost_scenarios_analysis.json")

if __name__ == "__main__":
    main()