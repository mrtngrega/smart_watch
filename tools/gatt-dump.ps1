# Read-only GATT dump of a BLE device (no writes). Usage: gatt-dump.ps1 -Mac 7802B728B519
param([string]$Mac='7802B728B519')
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op,$t){ $m=$asTask.MakeGenericMethod($t); $x=$m.Invoke($null,@($op)); $x.Wait(20000)|Out-Null; $x.Result }
$G='Windows.Devices.Bluetooth.GenericAttributeProfile'
[void][Windows.Devices.Bluetooth.BluetoothLEDevice,Windows.Devices.Bluetooth,ContentType=WindowsRuntime]
[void][Windows.Storage.Streams.DataReader,Windows.Storage.Streams,ContentType=WindowsRuntime]
$dev=Await ([Windows.Devices.Bluetooth.BluetoothLEDevice]::FromBluetoothAddressAsync([Convert]::ToUInt64($Mac,16))) ([Windows.Devices.Bluetooth.BluetoothLEDevice])
if(-not $dev){'device not found'; exit 1}
"name: $($dev.Name)  status: $($dev.ConnectionStatus)"
$svcs=Await ($dev.GetGattServicesAsync([Windows.Devices.Bluetooth.BluetoothCacheMode]::Uncached)) ([type]"$G.GattDeviceServicesResult, Windows.Devices.Bluetooth, ContentType=WindowsRuntime")
"services: $($svcs.Status) ($($svcs.Services.Count))"
foreach($s in $svcs.Services){
 "SERVICE $($s.Uuid)"
 $chs=Await ($s.GetCharacteristicsAsync([Windows.Devices.Bluetooth.BluetoothCacheMode]::Uncached)) ([type]"$G.GattCharacteristicsResult, Windows.Devices.Bluetooth, ContentType=WindowsRuntime")
 foreach($c in $chs.Characteristics){
  $line="  CHAR $($c.Uuid) props=$($c.CharacteristicProperties)"
  if($c.CharacteristicProperties.ToString() -match 'Read'){
   $r=Await ($c.ReadValueAsync()) ([type]"$G.GattReadResult, Windows.Devices.Bluetooth, ContentType=WindowsRuntime")
   if($r.Status -eq 'Success'){ $m=[Windows.Storage.Streams.DataReader].GetMethod("FromBuffer"); $rd=$m.Invoke($null,@($r.Value)); $n=[int]$r.Value.Length; $b=New-Object byte[] $n; $rd.ReadBytes($b); $line+=" value=$([BitConverter]::ToString($b))" } else { $line+=" read=$($r.Status)" }
  }
  $line
 }
}


