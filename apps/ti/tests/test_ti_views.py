import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import MagicMock, patch

User = get_user_model()

@pytest.fixture
def ti_user(db):
    return User.objects.create_user(
        username="ti_admin",
        password="password123",
        is_staff=True,
        is_superuser=True
    )

@pytest.fixture
def mock_diag():
    """Mock completo do módulo diagnostico para evitar chamadas de sistema."""
    with patch('apps.ti.views.diagnostico') as mock:
        mock.get_system_resources.return_value = {'cpu_percent': 10, 'ram_percent': 20}
        mock.get_db_stats.return_value = {'size': '10MB', 'tables': 50, 'vendor': 'sqlite'}
        mock.get_git_info.return_value = {'git_hash': 'abcdef1'}
        mock.check_external_integrations.return_value = []
        mock.check_ssl_expiry.return_value = {'days_left': 30}
        mock.get_topology_data.return_value = {}
        mock.get_orphan_files_count.return_value = 0
        mock.get_user_activity.return_value = {'sessoes_ativas': 5}
        mock.get_request_stats.return_value = {'latencia_media': '50ms', 'taxa_erro': '0%'}
        mock.get_security_health_score.return_value = 95
        mock.get_disk_breakdown.return_value = {}
        mock.get_slow_queries.return_value = []
        mock.get_comm_health.return_value = {}
        mock.get_task_queue_stats.return_value = {'pending': 0}
        mock.get_backup_status.return_value = {'last_backup': 'Nunca', 'size': '0MB', 'location': 'N/A'}
        mock.get_anomaly_status.return_value = {'status': 'OK', 'confidence': '100%', 'alerts_24h': 0}
        mock.get_lgpd_stats.return_value = {'pending_requests': 0}
        mock.get_security_audit_summary.return_value = {'2fa_adoption': '10%', 'weak_passwords': 0}
        mock.get_performance_heatmap.return_value = []
        mock.get_global_event_feed.return_value = []
        mock.get_db_connections.return_value = 5
        mock.get_cache_stats.return_value = {}
        yield mock

@pytest.mark.django_db
def test_painel_ti_access_mocked(client, ti_user, mock_diag):
    client.force_login(ti_user)
    url = reverse('ti:painel')
    response = client.get(url)
    assert response.status_code == 200
    assert b"v7.2.4" in response.content

@pytest.mark.django_db
def test_infraestrutura_ti_access_mocked(client, ti_user, mock_diag):
    client.force_login(ti_user)
    url = reverse('ti:infraestrutura')
    response = client.get(url)
    assert response.status_code == 200
    assert b"Hub de" in response.content

@pytest.mark.django_db
def test_api_logs_lgpd_mocked(client, ti_user, mock_diag):
    client.force_login(ti_user)
    url = reverse('ti:api_lgpd_logs')
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
