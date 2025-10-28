#!/usr/bin/env python3
"""
Framework Cost Calculator API
RESTful API wrapper for cost calculation functionality.
Designed for integration with web applications and external services.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cost_calculator import FrameworkCostCalculator, Framework, ModelProvider

class CostCalculatorAPI(BaseHTTPRequestHandler):
    """HTTP API handler for cost calculations"""
    
    def __init__(self, *args, **kwargs):
        self.calculator = FrameworkCostCalculator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)
        
        try:
            if path == "/":
                self._send_response(200, {"message": "Framework Cost Calculator API", "version": "1.0"})
            elif path == "/frameworks":
                self._handle_frameworks()
            elif path == "/models":
                self._handle_models()
            elif path == "/calculate":
                self._handle_calculate(params)
            elif path == "/compare":
                self._handle_compare(params)
            elif path == "/migration":
                self._handle_migration(params)
            else:
                self._send_response(404, {"error": "Endpoint not found"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            if path == "/calculate":
                self._handle_post_calculate(data)
            elif path == "/compare":
                self._handle_post_compare(data)
            elif path == "/migration":
                self._handle_post_migration(data)
            else:
                self._send_response(404, {"error": "Endpoint not found"})
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})
    
    def _handle_frameworks(self):
        """Return available frameworks"""
        frameworks = []
        for fw in Framework:
            metadata = self.calculator.framework_metadata[fw]
            frameworks.append({
                "id": fw.value,
                "name": fw.value.replace("_", " ").title(),
                "description": metadata["description"],
                "efficiency_score": metadata["efficiency_score"],
                "avg_tokens": metadata["avg_tokens_per_request"]
            })
        
        self._send_response(200, {"frameworks": frameworks})
    
    def _handle_models(self):
        """Return available models with pricing"""
        models = []
        for model in ModelProvider:
            pricing = self.calculator.model_pricing[model]
            models.append({
                "id": model.value,
                "name": model.value.replace("_", " ").upper(),
                "input_cost_per_1m": pricing.input_cost,
                "output_cost_per_1m": pricing.output_cost,
                "average_cost_per_1m": pricing.average_cost
            })
        
        self._send_response(200, {"models": models})
    
    def _handle_calculate(self, params):
        """Handle cost calculation via GET"""
        try:
            framework = Framework(params['framework'][0])
            model = ModelProvider(params['model'][0])
            requests = int(params['requests'][0])
            tokens = int(params.get('tokens', [None])[0]) if params.get('tokens') else None
            
            result = self.calculator.calculate_monthly_cost(framework, model, requests, tokens)
            self._send_response(200, result)
        except (KeyError, ValueError, IndexError) as e:
            self._send_response(400, {"error": f"Invalid parameters: {str(e)}"})
    
    def _handle_compare(self, params):
        """Handle framework comparison via GET"""
        try:
            model = ModelProvider(params['model'][0])
            requests = int(params['requests'][0])
            tokens = int(params.get('tokens', [None])[0]) if params.get('tokens') else None
            
            result = self.calculator.compare_frameworks(model, requests, tokens)
            self._send_response(200, {"comparison": result})
        except (KeyError, ValueError, IndexError) as e:
            self._send_response(400, {"error": f"Invalid parameters: {str(e)}"})
    
    def _handle_migration(self, params):
        """Handle migration analysis via GET"""
        try:
            from_fw = Framework(params['from'][0])
            to_fw = Framework(params['to'][0])
            model = ModelProvider(params['model'][0])
            requests = int(params['requests'][0])
            
            result = self.calculator.estimate_migration_savings(from_fw, to_fw, model, requests)
            self._send_response(200, result)
        except (KeyError, ValueError, IndexError) as e:
            self._send_response(400, {"error": f"Invalid parameters: {str(e)}"})
    
    def _handle_post_calculate(self, data):
        """Handle cost calculation via POST"""
        try:
            framework = Framework(data['framework'])
            model = ModelProvider(data['model'])
            requests = int(data['requests'])
            tokens = data.get('tokens')
            
            result = self.calculator.calculate_monthly_cost(framework, model, requests, tokens)
            self._send_response(200, result)
        except (KeyError, ValueError) as e:
            self._send_response(400, {"error": f"Invalid data: {str(e)}"})
    
    def _handle_post_compare(self, data):
        """Handle framework comparison via POST"""
        try:
            model = ModelProvider(data['model'])
            requests = int(data['requests'])
            tokens = data.get('tokens')
            
            result = self.calculator.compare_frameworks(model, requests, tokens)
            self._send_response(200, {"comparison": result})
        except (KeyError, ValueError) as e:
            self._send_response(400, {"error": f"Invalid data: {str(e)}"})
    
    def _handle_post_migration(self, data):
        """Handle migration analysis via POST"""
        try:
            from_fw = Framework(data['from'])
            to_fw = Framework(data['to'])
            model = ModelProvider(data['model'])
            requests = int(data['requests'])
            
            result = self.calculator.estimate_migration_savings(from_fw, to_fw, model, requests)
            self._send_response(200, result)
        except (KeyError, ValueError) as e:
            self._send_response(400, {"error": f"Invalid data: {str(e)}"})
    
    def _send_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    """Run the API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CostCalculatorAPI)
    print(f"🚀 Framework Cost Calculator API running on http://localhost:{port}")
    print("\nAvailable endpoints:")
    print("  GET  /                      - API info")
    print("  GET  /frameworks           - List frameworks")
    print("  GET  /models               - List models with pricing")
    print("  GET  /calculate?...        - Calculate costs")
    print("  GET  /compare?...          - Compare frameworks")
    print("  GET  /migration?...        - Migration analysis")
    print("  POST /calculate            - Calculate costs (JSON)")
    print("  POST /compare              - Compare frameworks (JSON)")
    print("  POST /migration            - Migration analysis (JSON)")
    print("\nExample usage:")
    print("  curl 'http://localhost:8000/calculate?framework=autogen&model=openai_gpt4o&requests=10000'")
    print("  curl 'http://localhost:8000/compare?model=openai_gpt4o&requests=10000'")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()