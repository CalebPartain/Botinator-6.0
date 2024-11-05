import requests

def get_csrf_token(session):
        response = session.get('https://cloud.samsara.com/r/auth/csrf')
        csrf_token = response.json().get('csrf_token')
        # Set CSRF token in cookies, if required
        session.cookies.set('csrf_token', csrf_token)
        return csrf_token

def login(session, email, password, csrf_token):
    url = 'https://cloud.samsara.com/r/auth/signin'

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://cloud.samsara.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
        "X-CSRF-Token": csrf_token
    }

    data = {
        'email': email,
        'password': password,
        'rememberMe': False
    }

    # Add CSRF token as a cookie if required
    session.cookies.set('X-CSRF-Token', csrf_token)

    response = session.post(url, headers=headers, json=data)
    print('Login status:', response.status_code)
    print('Login response:', response.text)  # Log response for debugging
    return response.status_code == 200

def request_data(session, csrf_token):
    url = "https://us9-ws.cloud.samsara.com/r/graphql?q=FleetHosReport"
    
    headers = {
        "accept": "application/json; version=2",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "cookie": f"samsara-session={session.cookies.get_dict().get('samsara-session', '')}",
        "origin": "https://cloud.samsara.com",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Opera GX";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
        "x-csrf-token": csrf_token
    }

    payload = {
        "query": """
            query FleetHosReport($groupId: int64!, $tagIds: [int64!], $durationMs: int64!, $endTime: int64, $hasRecapturedHoursReport: bool!, $useOriginalRecapHoursReport: bool!, $showDriversCategory: ShowDriversTypeEnum, $attributesQuery: [AttributesQuery_InputObject!], $showDriversVehicleAssignment: ShowDriversVehicleAssignmentEnum) {
            group(id: $groupId) {
                organization {
                name
                driverAppFeatureSettings {
                    hosEnabled
                }
                hasMissingVINsPrompt: hasFeature(featureKey: feature_missing_vins)
                hasFeatureBundleCMWarning: hasFeature(featureKey: bundle_cm_warning)
                }
                name
                carrierName
                carrierAddress
                drivers(
                tagIds: $tagIds
                showDriversCategory: $showDriversCategory
                attributesQuery: $attributesQuery
                showDriversVehicleAssignment: $showDriversVehicleAssignment
                durationMs: $durationMs
                ) {
                ...HosReportDriver
                }
                missingEldInfo {
                missingDOTNumber
                missingLicenseInfoCount
                missingVINVehicleList {
                    id
                }
                }
            }
            }

            fragment HosReportDriver on Driver {
            id
            name
            username
            deletedAt
            eldExempt
            timezone
            eldDayStartHour
            eldAlbertaHosEnabled
            hosLogsSummary(
                durationMs: $durationMs
                endMs: $endTime
                getGps: false
                checkConnectivity: true
            ) {
                driverName
                currentDutyStatusCode
                driverIsOffDuty
                timeInCurrentStatusMs
                vehicleId
                vehicleName
                timeUntilBreakMs
                maxTimeUntilBreakMs
                shiftDriveRemainingMs
                shiftRemainingMs
                cycleRemainingMs
                cycleTomorrowMs
                drivingInViolationTodayMs
                drivingInViolationCycleMs
                currentRulesetKey {
                geoState
                }
            }
            hosRecapturedTimes @include(if: $useOriginalRecapHoursReport) {
                recapturedDurationMs
                dayStartMs
            }
            currentVehicle(useIndex: true) @include(if: $hasRecapturedHoursReport) {
                location {
                formatted
                address {
                    name
                }
                }
            }
            canadaOilWellExemptionClaimEvent: lastExemptionClaimEvent(exemptionTypeId: 8) {
                endMs
            }
            }
        """,
        "variables": {
            "groupId": 69936,
            "durationMs": 864000000,
            "endTime": None,
            "tagIds": [],
            "hasRecapturedHoursReport": False,
            "useOriginalRecapHoursReport": False,
            "showDriversCategory": "activeDrivers",
            "showDriversVehicleAssignment": "allVehicles",
            "attributesQuery": []
        },
        "extensions": {
            "route": "/o/:org_id/fleet/reports/hos/driver",
            "orgId": "70368",
            "stashOutput": True,
            "storeDepSet": True
        }
    }

    response = session.post(url, headers=headers, json=payload)
    print('HOS request status:', response.status_code)
    if response.status_code == 200:
            response = response.json()
    else:
        print(response.text)  # Log error if request fails

    drivers = {}
    for driver in response['data']['group']['drivers']:
        if driver['deletedAt'] == '0001-01-01T00:00:00Z':
            drivers[driver['username']]= {
                            'driving_status':driver['hosLogsSummary']['currentDutyStatusCode'],
                            'time_in_current':driver['hosLogsSummary']['timeInCurrentStatusMs'],
                            'drive_time':driver['hosLogsSummary']['shiftDriveRemainingMs'],
                            'shiftRemainingMs':driver['hosLogsSummary']['shiftRemainingMs'],
                            'cycle_today':driver['hosLogsSummary']['cycleRemainingMs'],
                            'cycle_tomorrow':driver['hosLogsSummary']['cycleTomorrowMs']}
                
    return drivers


def get_driver_HOS(username, password):
    session = requests.Session()
    csrf_token = get_csrf_token(session)

    if login(session, username, password, csrf_token):
        print("Login successful")
        # Fetch Driver HOS data
        return request_data(session, csrf_token)
    