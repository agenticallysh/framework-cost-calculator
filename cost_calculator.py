#!/usr/bin/env python3
"""
Framework Cost Calculator
Real-time cost estimation for AI agent frameworks based on 2025 pricing data.
"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ModelProvider(Enum):
    OPENAI_GPT4O = "openai_gpt4o"
    OPENAI_GPT4O_MINI = "openai_gpt4o_mini"
    CLAUDE_35_SONNET = "claude_35_sonnet"
    LOCAL_LLM = "local_llm"

class Framework(Enum):
    AUTOGEN = "autogen"
    CREWAI = "crewai"
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"
    SEMANTIC_KERNEL = "semantic_kernel"

@dataclass
class PricingData:
    """2025 LLM Pricing Data (per 1M tokens)"""
    input_cost: float
    output_cost: float
    
    @property
    def average_cost(self) -> float:
        """Average cost assuming 60% input, 40% output token ratio"""
        return (self.input_cost * 0.6) + (self.output_cost * 0.4)

# Real 2025 pricing data
MODEL_PRICING = {
    ModelProvider.OPENAI_GPT4O: PricingData(5.00, 20.00),
    ModelProvider.OPENAI_GPT4O_MINI: PricingData(0.15, 0.60),
    ModelProvider.CLAUDE_35_SONNET: PricingData(3.00, 15.00),
    ModelProvider.LOCAL_LLM: PricingData(0.05, 0.05),
}

# Framework efficiency and overhead data
FRAMEWORK_METADATA = {
    Framework.SEMANTIC_KERNEL: {
        "avg_tokens_per_request": 1180 + 620,
        "efficiency_score": 0.96,
        "overhead_multiplier": 1.04,
        "description": "Enterprise integration"
    },
    Framework.AUTOGEN: {
        "avg_tokens_per_request": 1320 + 780,
        "efficiency_score": 0.93,
        "overhead_multiplier": 1.12,
        "description": "Research & development"
    },
    Framework.CREWAI: {
        "avg_tokens_per_request": 1450 + 850,
        "efficiency_score": 0.90,
        "overhead_multiplier": 1.15,
        "description": "Multi-agent systems"
    },
    Framework.LANGCHAIN: {
        "avg_tokens_per_request": 1580 + 950,
        "efficiency_score": 0.87,
        "overhead_multiplier": 1.16,
        "description": "Flexible applications"
    },
    Framework.LANGGRAPH: {
        "avg_tokens_per_request": 1680 + 1080,
        "efficiency_score": 0.84,
        "overhead_multiplier": 1.20,
        "description": "Stateful workflows"
    },
}

class FrameworkCostCalculator:
    """Real-time cost calculator for AI agent frameworks"""
    
    def __init__(self):
        self.model_pricing = MODEL_PRICING
        self.framework_metadata = FRAMEWORK_METADATA
    
    def calculate_cost_per_request(
        self, 
        framework: Framework, 
        model: ModelProvider,
        custom_tokens: Optional[int] = None
    ) -> float:
        """Calculate cost per request for given framework and model"""
        
        framework_data = self.framework_metadata[framework]
        pricing = self.model_pricing[model]
        
        # Use custom token count or framework average
        total_tokens = custom_tokens or framework_data["avg_tokens_per_request"]
        
        # Apply framework overhead
        adjusted_tokens = total_tokens * framework_data["overhead_multiplier"]
        
        # Calculate cost per million tokens, then scale to actual usage
        cost_per_million = pricing.average_cost
        cost_per_request = (adjusted_tokens / 1_000_000) * cost_per_million
        
        return cost_per_request
    
    def calculate_monthly_cost(
        self,
        framework: Framework,
        model: ModelProvider,
        requests_per_month: int,
        custom_tokens: Optional[int] = None
    ) -> Dict[str, float]:
        """Calculate comprehensive monthly costs"""
        
        # Base API costs
        cost_per_request = self.calculate_cost_per_request(framework, model, custom_tokens)
        api_cost = cost_per_request * requests_per_month
        
        # Infrastructure costs (based on usage tiers)
        infrastructure_cost = self._estimate_infrastructure_cost(requests_per_month)
        
        # Monitoring and observability
        monitoring_cost = self._estimate_monitoring_cost(requests_per_month)
        
        total_cost = api_cost + infrastructure_cost + monitoring_cost
        
        return {
            "api_cost": round(api_cost, 2),
            "infrastructure_cost": round(infrastructure_cost, 2),
            "monitoring_cost": round(monitoring_cost, 2),
            "total_cost": round(total_cost, 2),
            "cost_per_request": round(cost_per_request, 4)
        }
    
    def _estimate_infrastructure_cost(self, requests_per_month: int) -> float:
        """Estimate infrastructure costs based on usage"""
        if requests_per_month < 1000:
            return 35  # Basic tier
        elif requests_per_month < 10000:
            return 85 + (requests_per_month - 1000) * 0.01
        elif requests_per_month < 100000:
            return 320 + (requests_per_month - 10000) * 0.005
        else:
            return 850 + (requests_per_month - 100000) * 0.002
    
    def _estimate_monitoring_cost(self, requests_per_month: int) -> float:
        """Estimate monitoring and logging costs"""
        if requests_per_month < 1000:
            return 15
        elif requests_per_month < 10000:
            return 45
        elif requests_per_month < 100000:
            return 125
        else:
            return 250
    
    def compare_frameworks(
        self,
        model: ModelProvider,
        requests_per_month: int,
        custom_tokens: Optional[int] = None
    ) -> Dict[str, Dict]:
        """Compare costs across all frameworks"""
        
        results = {}
        for framework in Framework:
            results[framework.value] = self.calculate_monthly_cost(
                framework, model, requests_per_month, custom_tokens
            )
            results[framework.value]["framework_name"] = framework.value.replace("_", " ").title()
            results[framework.value]["description"] = self.framework_metadata[framework]["description"]
        
        # Sort by total cost
        sorted_results = dict(sorted(results.items(), key=lambda x: x[1]["total_cost"]))
        
        return sorted_results
    
    def estimate_migration_savings(
        self,
        from_framework: Framework,
        to_framework: Framework,
        model: ModelProvider,
        requests_per_month: int
    ) -> Dict[str, float]:
        """Calculate potential savings from framework migration"""
        
        current_cost = self.calculate_monthly_cost(from_framework, model, requests_per_month)
        new_cost = self.calculate_monthly_cost(to_framework, model, requests_per_month)
        
        monthly_savings = current_cost["total_cost"] - new_cost["total_cost"]
        annual_savings = monthly_savings * 12
        savings_percentage = (monthly_savings / current_cost["total_cost"]) * 100
        
        return {
            "current_monthly_cost": current_cost["total_cost"],
            "new_monthly_cost": new_cost["total_cost"],
            "monthly_savings": round(monthly_savings, 2),
            "annual_savings": round(annual_savings, 2),
            "savings_percentage": round(savings_percentage, 1)
        }

def main():
    """CLI interface for cost calculator"""
    calculator = FrameworkCostCalculator()
    
    print("🧮 AI Agent Framework Cost Calculator (2025)")
    print("=" * 50)
    
    # Example usage
    print("\n📊 Framework Comparison (10k requests/month, GPT-4o):")
    comparison = calculator.compare_frameworks(
        ModelProvider.OPENAI_GPT4O,
        10000
    )
    
    for framework, data in comparison.items():
        print(f"\n{data['framework_name']}: ${data['total_cost']}/month")
        print(f"  - API costs: ${data['api_cost']}")
        print(f"  - Infrastructure: ${data['infrastructure_cost']}")
        print(f"  - Monitoring: ${data['monitoring_cost']}")
        print(f"  - Cost per request: ${data['cost_per_request']}")
    
    # Migration example
    print("\n🔄 Migration Savings Example:")
    migration = calculator.estimate_migration_savings(
        Framework.LANGCHAIN,
        Framework.AUTOGEN,
        ModelProvider.OPENAI_GPT4O,
        10000
    )
    
    print(f"LangChain → AutoGen migration:")
    print(f"  - Current: ${migration['current_monthly_cost']}/month")
    print(f"  - New: ${migration['new_monthly_cost']}/month")
    print(f"  - Savings: ${migration['monthly_savings']}/month ({migration['savings_percentage']}%)")
    print(f"  - Annual savings: ${migration['annual_savings']}")

if __name__ == "__main__":
    main()