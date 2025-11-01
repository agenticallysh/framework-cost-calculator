#!/usr/bin/env python3
"""
Advanced ROI Calculator and Savings Analysis
Comprehensive financial analysis for AI framework investment decisions.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from cost_calculator import FrameworkCostCalculator, Framework, ModelProvider

@dataclass
class InvestmentScenario:
    """Investment scenario for ROI calculation"""
    framework: str
    initial_development_cost: float
    monthly_operating_cost: float
    team_size: int
    timeline_months: int
    risk_factor: float = 1.0  # 1.0 = normal risk, >1.0 = higher risk

@dataclass
class ROIResult:
    """ROI analysis result"""
    total_investment: float
    payback_period_months: Optional[float]
    roi_percentage: float
    npv: float
    annual_savings: float
    break_even_month: Optional[int]

class ROIAnalyzer:
    """Advanced ROI and savings analysis for framework selection"""
    
    def __init__(self):
        self.calculator = FrameworkCostCalculator()
        
        # Development cost estimates (in USD)
        self.development_costs = {
            "semantic_kernel": {
                "base_cost": 25000,
                "complexity_multiplier": 0.8,
                "description": "Lower complexity due to enterprise tooling and documentation"
            },
            "autogen": {
                "base_cost": 35000,
                "complexity_multiplier": 1.1,
                "description": "Medium complexity, advanced multi-agent features"
            },
            "crewai": {
                "base_cost": 30000,
                "complexity_multiplier": 1.0,
                "description": "Balanced complexity and capabilities"
            },
            "langchain": {
                "base_cost": 40000,
                "complexity_multiplier": 1.3,
                "description": "Higher complexity due to extensive customization needs"
            },
            "langgraph": {
                "base_cost": 45000,
                "complexity_multiplier": 1.4,
                "description": "Highest complexity due to stateful workflow management"
            }
        }
        
        # Risk factors for different scenarios
        self.risk_factors = {
            "startup": 1.3,      # Higher risk due to uncertainty
            "growth": 1.1,       # Moderate risk
            "enterprise": 0.9,   # Lower risk due to established processes
            "research": 1.2      # Higher risk due to experimental nature
        }
        
        # Discount rate for NPV calculations (annual)
        self.discount_rate = 0.10  # 10% annual discount rate
    
    def calculate_development_cost(
        self, 
        framework: str, 
        team_size: int, 
        complexity_factor: float = 1.0,
        timeline_months: int = 6
    ) -> float:
        """Calculate estimated development cost for framework implementation"""
        
        if framework not in self.development_costs:
            raise ValueError(f"Unknown framework: {framework}")
        
        base_data = self.development_costs[framework]
        base_cost = base_data["base_cost"]
        
        # Adjust for team size (economies of scale for larger teams)
        team_multiplier = 1.0 + (team_size - 3) * 0.15 if team_size > 3 else 1.0
        team_multiplier = min(team_multiplier, 2.0)  # Cap at 2x
        
        # Adjust for complexity
        complexity_cost = base_cost * base_data["complexity_multiplier"] * complexity_factor
        
        # Adjust for timeline (rushed timeline increases costs)
        if timeline_months < 4:
            timeline_multiplier = 1.4
        elif timeline_months < 6:
            timeline_multiplier = 1.2
        elif timeline_months > 12:
            timeline_multiplier = 0.9  # Longer timeline can reduce costs
        else:
            timeline_multiplier = 1.0
        
        total_cost = complexity_cost * team_multiplier * timeline_multiplier
        
        return round(total_cost, 2)
    
    def calculate_comprehensive_roi(
        self,
        current_framework: str,
        target_framework: str,
        model: ModelProvider,
        requests_per_month: int,
        team_size: int = 5,
        timeline_months: int = 6,
        analysis_period_months: int = 36,
        complexity_factor: float = 1.0,
        risk_scenario: str = "growth"
    ) -> Dict[str, Any]:
        """Calculate comprehensive ROI analysis for framework migration"""
        
        # Get monthly costs for both frameworks
        current_costs = self.calculator.calculate_monthly_cost(
            Framework(current_framework), model, requests_per_month
        )
        target_costs = self.calculator.calculate_monthly_cost(
            Framework(target_framework), model, requests_per_month
        )
        
        # Calculate development costs
        dev_cost = self.calculate_development_cost(
            target_framework, team_size, complexity_factor, timeline_months
        )
        
        # Apply risk factor
        risk_factor = self.risk_factors.get(risk_scenario, 1.0)
        adjusted_dev_cost = dev_cost * risk_factor
        
        # Calculate monthly savings
        monthly_savings = current_costs["total_cost"] - target_costs["total_cost"]
        
        # Calculate payback period
        if monthly_savings > 0:
            payback_months = adjusted_dev_cost / monthly_savings
        else:
            payback_months = None
        
        # Calculate NPV over analysis period
        npv = self._calculate_npv(
            adjusted_dev_cost, monthly_savings, analysis_period_months
        )
        
        # Calculate ROI
        total_savings = monthly_savings * analysis_period_months
        roi_percentage = ((total_savings - adjusted_dev_cost) / adjusted_dev_cost) * 100 if adjusted_dev_cost > 0 else 0
        
        # Generate cash flow projection
        cash_flow = self._generate_cash_flow_projection(
            adjusted_dev_cost, monthly_savings, analysis_period_months
        )
        
        # Calculate break-even analysis
        break_even_month = int(payback_months) + 1 if payback_months and payback_months > 0 else None
        
        result = {
            "migration_summary": {
                "from_framework": current_framework,
                "to_framework": target_framework,
                "model": model.value,
                "requests_per_month": requests_per_month,
                "analysis_period_months": analysis_period_months
            },
            "cost_analysis": {
                "current_monthly_cost": current_costs["total_cost"],
                "target_monthly_cost": target_costs["total_cost"],
                "monthly_savings": monthly_savings,
                "annual_savings": monthly_savings * 12,
                "development_cost": adjusted_dev_cost,
                "risk_factor": risk_factor
            },
            "roi_metrics": {
                "payback_period_months": payback_months,
                "roi_percentage": roi_percentage,
                "npv": npv,
                "break_even_month": break_even_month,
                "total_3_year_savings": monthly_savings * analysis_period_months
            },
            "cash_flow_projection": cash_flow,
            "recommendations": self._generate_roi_recommendations(
                monthly_savings, payback_months, roi_percentage, npv
            ),
            "generated_at": datetime.now().isoformat()
        }
        
        return result
    
    def _calculate_npv(
        self, 
        initial_investment: float, 
        monthly_cash_flow: float, 
        periods: int
    ) -> float:
        """Calculate Net Present Value"""
        monthly_discount_rate = (1 + self.discount_rate) ** (1/12) - 1
        
        npv = -initial_investment  # Initial investment is negative cash flow
        
        for month in range(1, periods + 1):
            discounted_cash_flow = monthly_cash_flow / ((1 + monthly_discount_rate) ** month)
            npv += discounted_cash_flow
        
        return round(npv, 2)
    
    def _generate_cash_flow_projection(
        self, 
        initial_investment: float, 
        monthly_savings: float, 
        periods: int
    ) -> List[Dict]:
        """Generate month-by-month cash flow projection"""
        cash_flow = []
        cumulative_cash_flow = -initial_investment
        
        for month in range(0, periods + 1):
            if month == 0:
                # Initial investment
                cash_flow.append({
                    "month": 0,
                    "description": "Initial Development Investment",
                    "cash_flow": -initial_investment,
                    "cumulative_cash_flow": cumulative_cash_flow
                })
            else:
                cumulative_cash_flow += monthly_savings
                cash_flow.append({
                    "month": month,
                    "description": f"Operational Savings Month {month}",
                    "cash_flow": monthly_savings,
                    "cumulative_cash_flow": cumulative_cash_flow
                })
        
        return cash_flow
    
    def _generate_roi_recommendations(
        self, 
        monthly_savings: float, 
        payback_months: Optional[float], 
        roi_percentage: float, 
        npv: float
    ) -> List[Dict]:
        """Generate actionable ROI recommendations"""
        recommendations = []
        
        # Payback analysis
        if payback_months is None or payback_months < 0:
            recommendations.append({
                "category": "Financial Risk",
                "level": "high",
                "message": "Migration will increase costs - not recommended from pure cost perspective",
                "action": "Consider non-financial benefits or alternative frameworks"
            })
        elif payback_months <= 12:
            recommendations.append({
                "category": "Quick ROI",
                "level": "positive",
                "message": f"Excellent payback period of {payback_months:.1f} months",
                "action": "Strong candidate for immediate migration"
            })
        elif payback_months <= 24:
            recommendations.append({
                "category": "Moderate ROI", 
                "level": "neutral",
                "message": f"Reasonable payback period of {payback_months:.1f} months",
                "action": "Consider migration if strategic benefits align"
            })
        else:
            recommendations.append({
                "category": "Long Payback",
                "level": "cautionary",
                "message": f"Long payback period of {payback_months:.1f} months",
                "action": "Evaluate strategic benefits beyond cost savings"
            })
        
        # NPV analysis
        if npv > 50000:
            recommendations.append({
                "category": "High Value",
                "level": "positive",
                "message": f"Excellent NPV of ${npv:,.0f}",
                "action": "Strong financial case for migration"
            })
        elif npv > 10000:
            recommendations.append({
                "category": "Positive Value",
                "level": "positive", 
                "message": f"Positive NPV of ${npv:,.0f}",
                "action": "Financially beneficial migration"
            })
        elif npv > -10000:
            recommendations.append({
                "category": "Break Even",
                "level": "neutral",
                "message": f"Near break-even NPV of ${npv:,.0f}",
                "action": "Consider strategic and operational benefits"
            })
        else:
            recommendations.append({
                "category": "Negative Value",
                "level": "cautionary",
                "message": f"Negative NPV of ${npv:,.0f}",
                "action": "Migration not recommended based on financial analysis"
            })
        
        # ROI percentage analysis
        if roi_percentage > 100:
            recommendations.append({
                "category": "Excellent ROI",
                "level": "positive",
                "message": f"Outstanding ROI of {roi_percentage:.1f}%",
                "action": "Prioritize this migration project"
            })
        elif roi_percentage > 50:
            recommendations.append({
                "category": "Good ROI",
                "level": "positive",
                "message": f"Strong ROI of {roi_percentage:.1f}%",
                "action": "Recommend proceeding with migration"
            })
        elif roi_percentage > 0:
            recommendations.append({
                "category": "Positive ROI",
                "level": "neutral",
                "message": f"Modest ROI of {roi_percentage:.1f}%",
                "action": "Consider if strategic benefits justify investment"
            })
        
        return recommendations
    
    def _perform_sensitivity_analysis(
        self,
        current_framework: str,
        target_framework: str,
        model: ModelProvider,
        base_requests: int,
        team_size: int,
        timeline_months: int,
        complexity_factor: float
    ) -> Dict[str, Any]:
        """Perform sensitivity analysis on key variables"""
        
        # Test different request volumes
        volume_scenarios = [
            base_requests * 0.5,   # 50% lower
            base_requests * 0.8,   # 20% lower
            base_requests,         # baseline
            base_requests * 1.2,   # 20% higher
            base_requests * 1.5    # 50% higher
        ]
        
        volume_analysis = []
        for volume in volume_scenarios:
            analysis = self.calculate_comprehensive_roi(
                current_framework, target_framework, model, 
                int(volume), team_size, timeline_months, 36, complexity_factor
            )
            volume_analysis.append({
                "volume": int(volume),
                "volume_change": ((volume - base_requests) / base_requests) * 100,
                "payback_months": analysis["roi_metrics"]["payback_period_months"],
                "roi_percentage": analysis["roi_metrics"]["roi_percentage"],
                "npv": analysis["roi_metrics"]["npv"]
            })
        
        # Test different complexity factors
        complexity_scenarios = [0.7, 0.9, 1.0, 1.2, 1.5]
        complexity_analysis = []
        for complexity in complexity_scenarios:
            analysis = self.calculate_comprehensive_roi(
                current_framework, target_framework, model,
                base_requests, team_size, timeline_months, 36, complexity
            )
            complexity_analysis.append({
                "complexity_factor": complexity,
                "development_cost": analysis["cost_analysis"]["development_cost"],
                "payback_months": analysis["roi_metrics"]["payback_period_months"],
                "roi_percentage": analysis["roi_metrics"]["roi_percentage"]
            })
        
        return {
            "volume_sensitivity": volume_analysis,
            "complexity_sensitivity": complexity_analysis,
            "key_insights": [
                "ROI is most sensitive to request volume changes",
                "Development complexity significantly impacts payback period",
                "Higher volumes make migration more attractive"
            ]
        }

def main():
    """Demo the ROI analyzer with comprehensive examples"""
    print("💰 Advanced ROI Calculator and Savings Analysis")
    print("=" * 55)
    
    analyzer = ROIAnalyzer()
    
    # Example: LangChain to Semantic Kernel migration
    print("\n📊 Example: LangChain → Semantic Kernel Migration")
    print("-" * 50)
    
    roi_analysis = analyzer.calculate_comprehensive_roi(
        current_framework="langchain",
        target_framework="semantic_kernel", 
        model=ModelProvider.OPENAI_GPT4O,
        requests_per_month=25000,
        team_size=8,
        timeline_months=6,
        analysis_period_months=36,
        complexity_factor=1.1,
        risk_scenario="growth"
    )
    
    # Display key results
    cost_analysis = roi_analysis["cost_analysis"]
    roi_metrics = roi_analysis["roi_metrics"]
    
    print(f"Monthly Savings: ${cost_analysis['monthly_savings']:.2f}")
    print(f"Annual Savings: ${cost_analysis['annual_savings']:.2f}")
    print(f"Development Cost: ${cost_analysis['development_cost']:,.0f}")
    print(f"Payback Period: {roi_metrics['payback_period_months']:.1f} months")
    print(f"ROI: {roi_metrics['roi_percentage']:.1f}%")
    print(f"NPV (3 years): ${roi_metrics['npv']:,.0f}")
    
    print(f"\n🎯 Recommendations:")
    for rec in roi_analysis["recommendations"]:
        level_emoji = {"positive": "✅", "neutral": "⚠️", "cautionary": "❌", "high": "🔴"}.get(rec["level"], "ℹ️")
        print(f"   {level_emoji} {rec['category']}: {rec['message']}")
        print(f"      Action: {rec['action']}")
    
    # Save detailed analysis
    with open("roi_analysis_example.json", "w") as f:
        json.dump(roi_analysis, f, indent=2)
    
    print(f"\n📄 Detailed analysis saved to: roi_analysis_example.json")
    
    # Show quick sensitivity analysis
    print(f"\n📈 Quick Sensitivity Analysis:")
    volumes = [15000, 25000, 35000]
    for volume in volumes:
        quick_analysis = analyzer.calculate_comprehensive_roi(
            "langchain", "semantic_kernel", ModelProvider.OPENAI_GPT4O,
            volume, 8, 6, 36, 1.1, "growth"
        )
        payback = quick_analysis["roi_metrics"]["payback_period_months"]
        volume_change = ((volume - 25000) / 25000) * 100
        print(f"   {volume_change:+.0f}% volume ({volume:,} req/month): {payback:.1f} month payback" if payback else f"   {volume_change:+.0f}% volume: No payback")

if __name__ == "__main__":
    main()