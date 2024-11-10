import subprocess
import time
import requests
import psycopg2

# constants for paths
NGINX_PATH = "./nginx"  # path to nginx directory
POSTGRES_PATH = "./postgres"  # path to postgres directory

# constants for ports and credentials
NGINX_PORT = 8080
POSTGRES_PORT = 5432
POSTGRES_USER = "test"
POSTGRES_PASSWORD = "test"
POSTGRES_DB = "test"

# functions
def run_command(command, cwd=None):
    """run a command in subprocess and check for cderrors"""
    try:
        result = subprocess.run(command, shell=True, check=True, cwd=cwd, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"error while executing command: {e.stderr}")
        raise

def build_docker_images():
    """build docker images"""
    print("building nginx image...")
    run_command("docker build -t custom-nginx .", cwd=NGINX_PATH)
    print("building postgres image...")
    run_command("docker build -t custom-postgres .", cwd=POSTGRES_PATH)
    print("build completed.")

def run_containers():
    """run containers"""
    print("starting nginx container...")
    run_command(f"docker run -d -p {NGINX_PORT}:80 --name test-nginx custom-nginx")
    print("starting postgres container...")
    run_command(f"docker run -d -p {POSTGRES_PORT}:5432 --name test-postgres custom-postgres")
    print("containers started.")

def test_nginx():
    """test nginx functionality"""
    time.sleep(5)  # wait for the container to start
    print("testing nginx...")

    # check if GET is forbidden
    response = requests.get(f"http://localhost:{NGINX_PORT}/api")
    assert response.status_code == 403, "GET request to /api should return 403 forbidden"

    # check if POST is allowed
    response = requests.post(f"http://localhost:{NGINX_PORT}/api")
    assert response.status_code in [200, 204], "POST request to /api should be allowed"

    print("nginx test passed successfully.")

def test_postgres():
    """test postgres functionality"""
    time.sleep(10)  # wait for the database to initialize
    print("testing postgres...")

    try:
        connection = psycopg2.connect(
            host="localhost",
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        assert cursor.fetchone()[0] == 1, "postgres SELECT 1 query should return 1"
        print("postgres test passed successfully.")
    except Exception as e:
        raise AssertionError(f"error connecting to postgres: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def cleanup():
    """remove containers and images"""
    print("cleaning up containers and images...")
    run_command("docker stop test-nginx test-postgres")
    run_command("docker rm test-nginx test-postgres")
    run_command("docker rmi custom-nginx custom-postgres")
    print("cleanup completed.")

# main process
if __name__ == "__main__":
    try:
        build_docker_images()
        run_containers()
        test_nginx()
        test_postgres()
        print("all tests passed successfully!")
    except Exception as e:
        print(f"error: {e}")
    finally:
        cleanup()