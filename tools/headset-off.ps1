# Disable the watch's classic audio/call profiles in Windows (A2DP, AVRCP, Hands-Free) so they stop holding the link.
# Needs admin. Undo: same script with -Enable. The BLE entries and the pairing stay.
param([switch]$Enable)
$ids = Get-PnpDevice | Where-Object {
    $_.InstanceId -match '7802B728B519' -and $_.InstanceId -match '\{0000(110B|110C|110E|111E)-'
} | Select-Object -ExpandProperty InstanceId
$ids += Get-PnpDevice | Where-Object { $_.FriendlyName -eq 'ARMODD Wr3(ID-B519) Hands-Free' -and $_.Class -eq 'MEDIA' } | Select-Object -ExpandProperty InstanceId
foreach ($id in $ids) {
    if ($Enable) { Enable-PnpDevice -InstanceId $id -Confirm:$false } else { Disable-PnpDevice -InstanceId $id -Confirm:$false }
    "$(if($Enable){'enabled'}else{'disabled'}) $id"
}
