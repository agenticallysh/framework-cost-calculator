#!/usr/bin/env python3
"""
Framework Cost Calculator Examples
Real-world scenarios and use cases with 2025 pricing data.
"""

from cost_calculator import FrameworkCostCalculator, Framework, ModelProvider

def main():
    calculator = FrameworkCostCalculator()
    
    print("🚀 Framework Cost Calculator - Real Examples")
    print("=" * 60)
    
    # Example 1: Startup with limited budget
    print("\n💡 Example 1: Startup (1,000 requests/month)")
    print("-" * 45)
    
    startup_comparison = calculator.compare_frameworks(
        ModelProvider.OPENAI_GPT4O_MINI,  # Cost-conscious choice
        1000
    )
    
    print("Most cost-effective options for startups:")
    for i, (framework, data) in enumerate(startup_comparison.items()):
        if i < 3:  # Top 3 cheapest
            print(f"{i+1}. {data['framework_name']}: ${data['total_cost']}/month")
            print(f"   Cost per request: ${data['cost_per_request']}")
    
    # Example 2: Enterprise deployment
    print("\n🏢 Example 2: Enterprise (50,000 requests/month)")
    print("-" * 50)
    
    enterprise_comparison = calculator.compare_frameworks(
        ModelProvider.OPENAI_GPT4O,
        50000
    )
    
    print("Enterprise-scale costs:")
    for framework, data in enterprise_comparison.items():
        print(f"• {data['framework_name']}: ${data['total_cost']:,}/month")
        print(f"  - API: ${data['api_cost']:,} | Infrastructure: ${data['infrastructure_cost']:,}")
    
    # Example 3: Migration analysis
    print("\n🔄 Example 3: Migration Cost Analysis")
    print("-" * 40)
    
    migrations = [
        (Framework.LANGCHAIN, Framework.AUTOGEN),
        (Framework.LANGGRAPH, Framework.CREWAI),
        (Framework.LANGCHAIN, Framework.SEMANTIC_KERNEL),
    ]
    
    for from_fw, to_fw in migrations:
        savings = calculator.estimate_migration_savings(
            from_fw, to_fw, ModelProvider.OPENAI_GPT4O, 10000
        )
        
        if savings['monthly_savings'] > 0:
            print(f"✅ {from_fw.value.title()} → {to_fw.value.title()}")
            print(f"   Monthly savings: ${savings['monthly_savings']} ({savings['savings_percentage']}%)")
            print(f"   Annual savings: ${savings['annual_savings']:,}")
        else:
            print(f"❌ {from_fw.value.title()} → {to_fw.value.title()}")
            print(f"   Additional cost: ${abs(savings['monthly_savings'])}/month")
    
    # Example 4: Model provider comparison
    print("\n🤖 Example 4: Model Provider Impact (CrewAI, 10k requests)")
    print("-" * 58)
    
    models = [
        (ModelProvider.OPENAI_GPT4O, "OpenAI GPT-4o"),
        (ModelProvider.OPENAI_GPT4O_MINI, "OpenAI GPT-4o Mini"),
        (ModelProvider.CLAUDE_35_SONNET, "Claude 3.5 Sonnet"),
        (ModelProvider.LOCAL_LLM, "Local LLM"),
    ]
    
    for model, name in models:
        cost_data = calculator.calculate_monthly_cost(
            Framework.CREWAI, model, 10000
        )
        print(f"• {name}: ${cost_data['total_cost']}/month")
        print(f"  API cost: ${cost_data['api_cost']} | Cost/request: ${cost_data['cost_per_request']}")
    
    # Example 5: Break-even analysis
    print("\n📊 Example 5: Usage Break-Even Points")
    print("-" * 42)
    
    usage_levels = [1000, 5000, 10000, 25000, 50000, 100000]
    
    print("Monthly costs by usage (AutoGen + GPT-4o):")
    for usage in usage_levels:
        cost_data = calculator.calculate_monthly_cost(
            Framework.AUTOGEN, ModelProvider.OPENAI_GPT4O, usage
        )
        cost_per_1k = (cost_data['total_cost'] / usage) * 1000
        print(f"• {usage:,} requests: ${cost_data['total_cost']:,.0f}/month (${cost_per_1k:.2f}/1k)")
    
    # Example 6: ROI calculation
    print("\n💰 Example 6: ROI Analysis")
    print("-" * 30)
    
    # Typical customer support automation scenario
    manual_cost_per_month = 8500  # Human agents
    automation_cost = calculator.calculate_monthly_cost(
        Framework.CREWAI, ModelProvider.OPENAI_GPT4O, 5000
    )
    
    monthly_savings = manual_cost_per_month - automation_cost['total_cost']
    roi_percentage = (monthly_savings / automation_cost['total_cost']) * 100
    payback_period = automation_cost['total_cost'] / monthly_savings
    
    print(f"Customer Support Automation (5k conversations/month):")
    print(f"• Manual process cost: ${manual_cost_per_month:,}/month")
    print(f"• Automation cost: ${automation_cost['total_cost']:,.0f}/month")
    print(f"• Monthly savings: ${monthly_savings:,.0f}")
    print(f"• ROI: {roi_percentage:.0f}%")
    print(f"• Payback period: {payback_period:.1f} months")

if __name__ == "__main__":
    main()