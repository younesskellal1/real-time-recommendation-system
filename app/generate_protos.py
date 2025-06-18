import os
import subprocess
import sys

def generate_proto_files():
    # Obtenir le chemin absolu du répertoire courant
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_dir = os.path.join(current_dir, 'protos')
    proto_file = os.path.join(proto_dir, 'recommendation.proto')
    
    # Créer le dossier protos s'il n'existe pas
    os.makedirs(proto_dir, exist_ok=True)
    
    # Générer les fichiers Python à partir du proto file
    subprocess.run([
        'python', '-m', 'grpc_tools.protoc',
        f'--proto_path={proto_dir}',
        f'--python_out={proto_dir}',
        f'--grpc_python_out={proto_dir}',
        proto_file
    ])
    
    # Modifier les imports dans les fichiers générés
    pb2_file = os.path.join(proto_dir, 'recommendation_pb2.py')
    pb2_grpc_file = os.path.join(proto_dir, 'recommendation_pb2_grpc.py')
    
    # Modifier recommendation_pb2_grpc.py
    if os.path.exists(pb2_grpc_file):
        with open(pb2_grpc_file, 'r') as f:
            content = f.read()
        
        # Remplacer l'import
        content = content.replace(
            'import recommendation_pb2 as recommendation__pb2',
            'from app.protos import recommendation_pb2 as recommendation__pb2'
        )
        
        with open(pb2_grpc_file, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    generate_proto_files() 