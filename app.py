#!/usr/bin/env python3
"""
Interactive Web Interface for Framework Cost Calculator
Flask-based web application with real-time cost calculations and comparisons.
"""

from flask import Flask, render_template, request, jsonify
import json
from cost_calculator import FrameworkCostCalculator, Framework, ModelProvider

app = Flask(__name__)
calculator = FrameworkCostCalculator()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_costs():
    """API endpoint for cost calculation"""
    try:
        data = request.get_json()
        
        framework = Framework(data['framework'])
        model = ModelProvider(data['model'])
        requests_per_month = int(data['requests_per_month'])
        custom_tokens = data.get('custom_tokens')
        
        if custom_tokens:
            custom_tokens = int(custom_tokens)
        
        result = calculator.calculate_monthly_cost(
            framework, model, requests_per_month, custom_tokens
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/compare', methods=['POST'])
def compare_frameworks():
    """API endpoint for framework comparison"""
    try:
        data = request.get_json()
        
        model = ModelProvider(data['model'])
        requests_per_month = int(data['requests_per_month'])
        custom_tokens = data.get('custom_tokens')
        
        if custom_tokens:
            custom_tokens = int(custom_tokens)
        
        results = calculator.compare_frameworks(
            model, requests_per_month, custom_tokens
        )
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/migration', methods=['POST'])
def calculate_migration():
    """API endpoint for migration cost analysis"""
    try:
        data = request.get_json()
        
        from_framework = Framework(data['from_framework'])
        to_framework = Framework(data['to_framework'])
        model = ModelProvider(data['model'])
        requests_per_month = int(data['requests_per_month'])
        
        result = calculator.estimate_migration_savings(
            from_framework, to_framework, model, requests_per_month
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/models')
def get_models():
    """Get available models and their pricing"""
    models = {}
    for model in ModelProvider:
        pricing = calculator.model_pricing[model]
        models[model.value] = {
            'name': model.value.replace('_', ' ').title(),
            'input_cost': pricing.input_cost,
            'output_cost': pricing.output_cost,
            'average_cost': pricing.average_cost
        }
    
    return jsonify(models)

@app.route('/api/frameworks')
def get_frameworks():
    """Get available frameworks and their metadata"""
    frameworks = {}
    for framework in Framework:
        metadata = calculator.framework_metadata[framework]
        frameworks[framework.value] = {
            'name': framework.value.replace('_', ' ').title(),
            'description': metadata['description'],
            'avg_tokens': metadata['avg_tokens_per_request'],
            'efficiency': metadata['efficiency_score'],
            'overhead': metadata['overhead_multiplier']
        }
    
    return jsonify(frameworks)

@app.route('/scenarios')
def scenarios():
    """Cost scenarios page"""
    return render_template('scenarios.html')

@app.route('/migration')
def migration():
    """Migration calculator page"""
    return render_template('migration.html')

@app.route('/api')
def api_docs():
    """API documentation page"""
    return render_template('api.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)